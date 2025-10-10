#ifndef HPCG_NO_OPENMP
#include <omp.h>
#endif

#include <cassert>
#include "GenerateCoarseProblem.hpp"
#include "GenerateGeometry.hpp"
#include "GenerateProblem.hpp"
#include "SetupHalo.hpp"

void GenerateCoarseProblem(const SparseMatrix & Af) {
  // Make local copies of geometry information
  global_int_t nxf = Af.geom->nx;
  global_int_t nyf = Af.geom->ny;
  global_int_t nzf = Af.geom->nz;

  // Ensure fine grid dimensions are divisible by 2
  assert(nxf % 2 == 0);
  assert(nyf % 2 == 0);
  assert(nzf % 2 == 0);

  // Compute coarse grid sizes
  local_int_t nxc = nxf / 2;
  local_int_t nyc = nyf / 2;
  local_int_t nzc = nzf / 2;

  // Number of coarse grid rows
  local_int_t localNumberOfCoarseRows = nxc * nyc * nzc;
  assert(localNumberOfCoarseRows > 0);

  // Allocate f2cOperator based on coarse rows
  local_int_t * f2cOperator = new local_int_t[localNumberOfCoarseRows];

  // Initialize f2cOperator
#ifndef HPCG_NO_OPENMP
  #pragma omp parallel for
#endif
  for (local_int_t i = 0; i < localNumberOfCoarseRows; ++i) {
    f2cOperator[i] = 0;
  }

  // Populate f2cOperator mapping from coarse row to fine row
#ifndef HPCG_NO_OPENMP
  #pragma omp parallel for collapse(3)
#endif
  for (local_int_t izc = 0; izc < nzc; ++izc) {
    for (local_int_t iyc = 0; iyc < nyc; ++iyc) {
      for (local_int_t ixc = 0; ixc < nxc; ++ixc) {
        local_int_t izf = 2 * izc;
        local_int_t iyf = 2 * iyc;
        local_int_t ixf = 2 * ixc;

        local_int_t currentCoarseRow = izc * nyc * nxc + iyc * nxc + ixc;
        local_int_t currentFineRow = izf * nyf * nxf + iyf * nxf + ixf;

        f2cOperator[currentCoarseRow] = currentFineRow;
      }
    }
  }

  // Create coarse geometry
  Geometry * geomc = new Geometry;
  local_int_t zlc = 0, zuc = 0;
  int pz = Af.geom->pz;

  if (pz > 0) {
    zlc = Af.geom->partz_nz[0] / 2;
    zuc = Af.geom->partz_nz[1] / 2;
  }

  GenerateGeometry(
    Af.geom->size, Af.geom->rank, Af.geom->numThreads,
    Af.geom->pz, zlc, zuc, nxc, nyc, nzc,
    Af.geom->npx, Af.geom->npy, Af.geom->npz, geomc
  );

  // Construct coarse matrix
  SparseMatrix * Ac = new SparseMatrix;
  InitializeSparseMatrix(*Ac, geomc);
  GenerateProblem(*Ac, nullptr, nullptr, nullptr);
  SetupHalo(*Ac);

  // Allocate and initialize vectors
  Vector * rc = new Vector;
  Vector * xc = new Vector;
  Vector * Axf = new Vector;

  InitializeVector(*rc, localNumberOfCoarseRows);  // matches f2cOperator size
  InitializeVector(*xc, Ac->localNumberOfColumns);
  InitializeVector(*Axf, Af.localNumberOfColumns);

  // Link coarse matrix and multigrid data
  Af.Ac = Ac;
  MGData * mgData = new MGData;
  InitializeMGData(f2cOperator, rc, xc, Axf, *mgData);
  Af.mgData = mgData;
}
