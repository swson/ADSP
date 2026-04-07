#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sched.h>
#include <stdint.h>

#include "pmu.h"

static int is_rank_zero(void)
{
    const char *r = getenv("OMPI_COMM_WORLD_RANK");  /* OpenMPI */
    if (!r) r = getenv("PMI_RANK");                  /* MPICH / Intel MPI */
    if (!r) r = getenv("SLURM_PROCID");              /* Slurm-launched MPI */
    if (!r) return 1;   /* not under MPI → treat as rank 0 */
    return atoi(r) == 0;
}

static int    ts_mode        = 0;
static int    ts_interval_ms = 1000;
static FILE  *ts_fp          = NULL;

#define barrier() __asm__ __volatile__("": : :"memory")

inline uint64_t rdpmc(int fixed, int index) {
    uint64_t a, d, c = (fixed ? (0x4000 << 16) : 0) | index;
    barrier();
    __asm __volatile("lfence;"
                     "rdpmc;"
                     : "=a"(a), "=d"(d)
                     : "c"(c));
    barrier();
    return (d << 32) | a;
}

inline int wrmsr(struct pmu_ctx *p, uint64_t val, off_t offset) {
    return pwrite(p->fd, &val, sizeof(val), offset) != sizeof(val);
}

int pmu_init(struct pmu_ctx *p) {
    int cpu;
    char buf[18];
    uint64_t eax = 10, edx;

    char *mode = getenv("HPCG_PMU_MODE");
    if (mode && strcmp(mode, "timeseries") == 0) {
        ts_mode = 1;

        char *interval = getenv("HPCG_PMU_INTERVAL_MS");
        if (interval)
            ts_interval_ms = atoi(interval);

        /* ── CHANGED ────────────────────────────────────────────────────── *
         * BEFORE: every rank called fopen() on the same filename,           *
         *         causing N processes to write to the same file             *
         *         → interleaved headers and duplicate rows.                 *
         *                                                                   *
         * AFTER:  wrapped in is_rank_zero() so only rank 0 opens the file.  *
         *         Non-zero ranks leave ts_fp = NULL and do nothing.         *
         * ─────────────────────────────────────────────────────────────────  */
        if (is_rank_zero()) {                              /* ← ADDED guard */
            char *outfile = getenv("HPCG_PMU_OUTFILE");
            if (outfile) {
                ts_fp = fopen(outfile, "w");
                if (!ts_fp) {
                    perror("fopen");
                    return errno ? errno : -1;
                }
            } else {
                fprintf(stderr, "HPCG_PMU_OUTFILE not set in timeseries mode\n");
                return -1;
            }
        }
        /* Non-zero ranks: ts_fp stays NULL — they never write anything */
    }

    __asm __volatile("cpuid" : "+a"(eax), "=d"(edx)::"ebx", "ecx");

    p->nfcntrs = edx & 0x0f;
    edx >>= 5;
    p->fcntrw = edx;
    p->ver = eax;
    eax >>= 8;
    p->npcntrs = eax;
    eax >>= 8;
    p->pcntrw = eax;

    cpu_set_t mask;
    cpu = sched_getcpu();
    CPU_ZERO(&mask);
    CPU_SET(cpu, &mask);

    if (sched_setaffinity(0, sizeof(cpu_set_t), &mask) < 0) {
        perror("sched_setaffinity");
        return errno;
    }

    sprintf(buf, "/dev/cpu/%d/msr", cpu);
    if ((p->fd = open(buf, O_RDWR)) < 0) {
        perror("open");
        return errno;
    }

    return 0;
}

int pmu_clear(struct pmu_ctx *p) {
    /* UNCHANGED */
    int ret;
    uint64_t mask = 0;

    if ((ret = wrmsr(p, 0, IA32_PERF_GLOBAL_CTRL)))
        return ret;
    if ((ret = wrmsr(p, 0, IA32_FIXED_CTR_CTRL)))
        return ret;

    for (char i = 0; i < p->npcntrs; ++i) {
        if ((ret = wrmsr(p, 0, IA32_PERFEVTSEL0 + i)))
            return ret;
        mask |= (1 << i);
    }

    for (char i = 0; i < p->nfcntrs; ++i) {
        if ((ret = wrmsr(p, 0, IA32_FIXED_CTR0 + i)))
            return ret;
        mask |= (1ULL << (34 - i));
    }

    return wrmsr(p, mask, IA32_PERF_GLOBAL_CTRL);
}

int pmu_trace(struct pmu_ctx *p, union counter_config *const events, int n) {
    int ret = 0;
    n = n > p->npcntrs ? p->npcntrs : n;

    if (ts_mode) {
        /* ── CHANGED ────────────────────────────────────────────────────── *
         * BEFORE: every rank called perf_ts_start(), so N sampler threads   *
         *         were spawned, all writing to the same FILE*.               *
         *                                                                   *
         * AFTER:  non-zero ranks return 0 immediately.                      *
         *         Only rank 0 (which has a valid ts_fp) starts the sampler. *
         * ─────────────────────────────────────────────────────────────────  */
        if (!is_rank_zero()) return 0;                     /* ← ADDED guard */
        return perf_ts_start(ts_fp, ts_interval_ms);
    }

    if ((ret = wrmsr(p, 0x222, IA32_FIXED_CTR_CTRL)))
        return ret;

    for (int i = 0; i < n; ++i)
        if ((ret = wrmsr(p, events[i].val, IA32_PERFEVTSEL0 + i)))
            return ret;

    return 0;
}

void pmu_read(struct pmu_ctx *p, uint64_t *vals, int n) {
    /* UNCHANGED */
    n = n > p->npcntrs ? p->npcntrs : n;

    for (int i = 0; i < p->nfcntrs; ++i)
        vals[i] = rdpmc(1, i);

    vals += p->nfcntrs;

    for (int i = 0; i < n; ++i)
        vals[i] = rdpmc(0, i);
}

int pmu_exit(struct pmu_ctx *p) {
    if (ts_mode) {
        /* ── CHANGED ────────────────────────────────────────────────────── *
         * BEFORE: every rank called perf_ts_stop() and fclose(),            *
         *         causing double-free / double-close on the same fd/FILE*.  *
         *                                                                   *
         * AFTER:  only rank 0 stops the sampler and closes the file.        *
         * ─────────────────────────────────────────────────────────────────  */
        if (is_rank_zero()) {                              /* ← ADDED guard */
            perf_ts_stop();
            if (ts_fp) {
                fclose(ts_fp);
                ts_fp = NULL;
            }
        }
    }

    return close(p->fd);
}
