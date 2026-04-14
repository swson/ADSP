/* perf_ts.c
 *
 * Continuously samples 4 hardware PMU counters for the current process
 * and writes time-series CSV rows to a file.
 *
 * Columns: timestamp_ms, bus_cycles, cache_references, cache_misses, branch_misses
 *
 */

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <stdint.h>
#include <stdlib.h>
#include <sched.h>
#include <errno.h>

/* ── syscall wrapper ────────────────────────────────────────────────────── */
static int perf_event_open(struct perf_event_attr *hw_event,
                           pid_t pid, int cpu,
                           int group_fd, unsigned long flags)
{
    return (int)syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
}

/* ── 4 counters to track ────────────────────────────────────────────────── */
#define NUM_COUNTERS 4

static const struct {
    uint32_t    type;
    uint64_t    config;
    const char *label;
} counter_defs[NUM_COUNTERS] = {
    { PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES,       "cpu_cycles"       },
    { PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_REFERENCES, "cache_references" },
    { PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_MISSES,     "cache_misses"     },
    { PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES,    "branch_misses"    },
};

/* ── internal state ─────────────────────────────────────────────────────── */
static int          fd[NUM_COUNTERS] = {-1,-1,-1,-1};   /* one perf fd per counter          */
static volatile int stop_flag      = 0;
static pthread_t    sampler_thread;
static int          thread_started = 0;
static int          header_written = 0; /* write CSV header only once       */

struct sampler_args {
    FILE *fp;
    int   interval_ms;
};

/* ── sampler thread ─────────────────────────────────────────────────────── */
static void *sampler_func(void *arg)
{
    struct sampler_args *args = (struct sampler_args *)arg;

    while (!stop_flag) {

        /* 1. read all 4 counters */
        uint64_t vals[NUM_COUNTERS];
        int read_ok = 1;
        for (int i = 0; i < NUM_COUNTERS; i++) {
	    if (fd[i] == -1) { vals[i] = 0; continue; }   /* skipped counter */
            if (read(fd[i], &vals[i], sizeof(uint64_t))
                    != (ssize_t)sizeof(uint64_t)) {
                if (errno == EINTR) { read_ok = 0; break; }
                perror("perf read");
                read_ok = 0;
                break;
            }
        }
        if (!read_ok) continue;

        /* 2. wall-clock timestamp in milliseconds */
        struct timespec ts;
        if (clock_gettime(CLOCK_MONOTONIC, &ts) == -1) {
            perror("clock_gettime");
            break;
        }
        long long ts_ms = (long long)ts.tv_sec * 1000LL
                        + ts.tv_nsec / 1000000LL;

        /* 3. write one CSV row: timestamp, cycles, instructions,
                                 cache_refs, cache_misses          */
        fprintf(args->fp, "%lld,%llu,%llu,%llu,%llu\n",
                ts_ms,
                (unsigned long long)vals[0],
                (unsigned long long)vals[1],
                (unsigned long long)vals[2],
                (unsigned long long)vals[3]);
        fflush(args->fp);

        /* 4. sleep for requested interval, resume on EINTR */
        struct timespec sleep_ts = {
            .tv_sec  =  args->interval_ms / 1000,
            .tv_nsec = (args->interval_ms % 1000) * 1000000L
        };
        struct timespec rem;
        while (nanosleep(&sleep_ts, &rem) == -1 && errno == EINTR)
            sleep_ts = rem;
    }

    free(args);
    return NULL;
}

/* ── public API ─────────────────────────────────────────────────────────── */

/*
 * perf_ts_start() – open 4 CPU perf counters and start the sampler thread.
 *
 * Safe to call multiple times — silently skips if already running.
 * Header is written only on the very first call.
 *
 * @fp          Open writable FILE* for CSV output.
 * @interval_ms Sampling interval in ms. Default 500 if <= 0.
 * Returns 0 on success, -1 on error.
 */
int perf_ts_start(FILE *fp, int interval_ms)
{
    struct sampler_args *args = NULL;
    int rc = 0;

    /* silent reentry guard — pmu_trace() calls this once per CG iteration */
    if (thread_started) return 0;

    fprintf(stderr, "perf_ts_start called: interval_ms=%d\n", interval_ms);
    fflush(stderr);

    if (!fp) {
        fprintf(stderr, "perf_ts_start: fp is NULL\n");
        errno = EINVAL;
        return -1;
    }

    if (interval_ms <= 0)
        interval_ms = 500;

    /* write CSV header exactly once across all calls */
    if (!header_written) {
//        header_written = 1;   // set BEFORE writing to prevent races
        fprintf(fp, "timestamp_ms");
        for (int i = 0; i < NUM_COUNTERS; i++)
            fprintf(fp, ",%s", counter_defs[i].label);
        fprintf(fp, "\n");
        fflush(fp);
        header_written = 1;
    }

    /* ── open one perf fd per counter ──────────────────────────────────── *
     *  pid = getpid()  →  this process (rank 0)                            *
     *  cpu = -1        →  follow across CPU migrations                     *
     *  inherit = 1     →  include OpenMP child threads                     *
     * ─────────────────────────────────────────────────────────────────── */
    for (int i = 0; i < NUM_COUNTERS; i++) {
        struct perf_event_attr pe;
        memset(&pe, 0, sizeof(pe));
        pe.type           = counter_defs[i].type;
        pe.size           = sizeof(pe);
        pe.config         = counter_defs[i].config;
        pe.disabled       = 1;
        pe.exclude_kernel = 0;
        pe.exclude_hv     = 0;
        pe.inherit        = 1;

	int cpu = sched_getcpu();
	if (cpu < 0) {
	    perror("sched_getcpu");
	    goto cleanup;
	}

//	fd[i] = perf_event_open(&pe, 0, -1, -1, 0);
//	fprintf(stderr, "[PMU DEBUG] counter[%d] fd=%d errno=%d\n", i, fd[i], errno);
        fd[i] = perf_event_open(&pe, -1, 0, -1, 0);
	fprintf(stderr, "[PMU DEBUG] counter[%d] fd=%d errno=%d\n", i, fd[i], errno);
//        fd[i] = perf_event_open(&pe, -1, cpu, -1, 0);
       // fd[i] = perf_event_open(&pe, getpid(), -1, -1, 0);
      /*   if (fd[i] == -1) {
    		fprintf(stderr,
		        "WARNING: counter [%s] not available on this CPU/VM, "
		        "skipping (column will show 0)\n",
		        counter_defs[i].label);
		    fd[i] = -1;   // mark as skipped, don't abort 
		    continue;
	}
     }
    // reset and enable all counters atomically 
    for (int i = 0; i < NUM_COUNTERS; i++) {
        if (ioctl(fd[i], PERF_EVENT_IOC_RESET,  0) == -1) {
            perror("ioctl RESET"); goto cleanup;
        }
        if (ioctl(fd[i], PERF_EVENT_IOC_ENABLE, 0) == -1) {
            perror("ioctl ENABLE"); goto cleanup;
        }
    }
*/
	for (int i = 0; i < NUM_COUNTERS; i++) {
	    if (fd[i] == -1) continue;
	    if (ioctl(fd[i], PERF_EVENT_IOC_RESET, 0) == -1) { perror("ioctl RESET"); goto cleanup; }
	    if (ioctl(fd[i], PERF_EVENT_IOC_ENABLE, 0) == -1) { perror("ioctl ENABLE"); goto cleanup; }
	}
}

    /* launch sampler thread */
    stop_flag = 0;

    args = (struct sampler_args *)malloc(sizeof(*args));  
    if (!args) {
        perror("malloc");
        goto cleanup;
    }
    args->fp          = fp;
    args->interval_ms = interval_ms;

    rc = pthread_create(&sampler_thread, NULL, sampler_func, args);
    if (rc != 0) {
        errno = rc;
        perror("pthread_create");
        free(args);
        goto cleanup;
    }

    thread_started = 1;
    return 0;

cleanup:
    for (int i = 0; i < NUM_COUNTERS; i++) {
        if (fd[i] != -1) {
            ioctl(fd[i], PERF_EVENT_IOC_DISABLE, 0);
            close(fd[i]);
            fd[i] = -1;
        }
    }
    return -1;
}

/*
 * perf_ts_stop() – stop sampler thread, disable and close all perf fds.
 * Safe to call even if perf_ts_start() was never called or failed.
 */
void perf_ts_stop(void)
{
    stop_flag = 1;

    if (thread_started) {
        pthread_join(sampler_thread, NULL);
        thread_started = 0;
    }

    for (int i = 0; i < NUM_COUNTERS; i++) {
        if (fd[i] != -1) {
            ioctl(fd[i], PERF_EVENT_IOC_DISABLE, 0);
            close(fd[i]);
            fd[i] = -1;
        }
    }
}
