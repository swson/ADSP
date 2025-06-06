//@HEADER
// ***************************************************
//
// HPCG: High Performance Conjugate Gradient Benchmark
//
// Contact:
// Michael A. Heroux (maherou@sandia.gov)
// Jack Dongarra     (dongarra@eecs.utk.edu)
// Piotr Luszczek    (luszczek@eecs.utk.edu)
//
// ***************************************************
//@HEADER

#include "CheckProblem.hpp"
#include "SparseMatrix.hpp"
#include "Vector.hpp"
#include "Geometry.hpp"
#include <cassert>
#include <iostream>

#ifndef HPCG_NO_MPI
#include <mpi.h>
#endif

#ifndef HPCG_NO_OPENMP
#include <omp.h>
#endif

void CheckProblem(SparseMatrix & A, Vector * b, Vector * x, Vector * xexact) {
  // Make local copies of geometry info
  global_int_t nx = A.geom->nx;
  global_int_t ny = A.geom->ny;
  global_int_t nz = A.geom->nz;
  global_int_t gnx = A.geom->gnx;
  global_int_t gny = A.geom->gny;
  global_int_t gnz = A.geom->gnz;
  global_int_t gix0 = A.geom->gix0;
  global_int_t giy0 = A.geom->giy0;
  global_int_t giz0 = A.geom->giz0;

  local_int_t localNumberOfRows = nx * ny * nz;
  global_int_t totalNumberOfRows = gnx * gny * gnz;

  local_int_t localNumberOfNonzeros = 0;

#ifndef HPCG_NO_OPENMP
#pragma omp parallel for reduction(+:localNumberOfNonzeros)
#endif
  for (local_int_t iz = 0; iz < nz; iz++) {
    global_int_t giz = giz0 + iz;
    for (local_int_t iy = 0; iy < ny; iy++) {
      global_int_t giy = giy0 + iy;
      for (local_int_t ix = 0; ix < nx; ix++) {
        global_int_t gix = gix0 + ix;
        local_int_t currentLocalRow = iz * nx * ny + iy * nx + ix;
        global_int_t currentGlobalRow = giz * gnx * gny + giy * gnx + gix;

        assert(A.localToGlobalMap[currentLocalRow] == currentGlobalRow);

        char numberOfNonzerosInRow = 0;
        std::vector<double> &currentValues = A.matrixValues[currentLocalRow];
        std::vector<global_int_t> &currentIndices = A.mtxIndG[currentLocalRow];
        size_t idx = 0;

        for (int sz = -1; sz <= 1; sz++) {
          if (giz + sz > -1 && giz + sz < gnz) {
            for (int sy = -1; sy <= 1; sy++) {
              if (giy + sy > -1 && giy + sy < gny) {
                for (int sx = -1; sx <= 1; sx++) {
                  if (gix + sx > -1 && gix + sx < gnx) {
                    global_int_t curcol = currentGlobalRow + sz * gnx * gny + sy * gnx + sx;

                    if (curcol == currentGlobalRow) {
                      assert(A.matrixDiagonal[currentLocalRow] == &currentValues[idx]);
                      assert(currentValues[idx++] == 26.0);
                    } else {
                      assert(currentValues[idx++] == -1.0);
                    }

                    assert(currentIndices[idx - 1] == curcol);
                    numberOfNonzerosInRow++;
                  }
                }
              }
            }
          }
        }

        assert(A.nonzerosInRow[currentLocalRow] == numberOfNonzerosInRow);

        if (b) assert(b->values[currentLocalRow] == 26.0 - ((double)(numberOfNonzerosInRow - 1)));
        if (x) assert(x->values[currentLocalRow] == 0.0);
        if (xexact) assert(xexact->values[currentLocalRow] == 1.0);

        localNumberOfNonzeros += numberOfNonzerosInRow;
      }
    }
  }

  global_int_t totalNumberOfNonzeros = 0;
#ifndef HPCG_NO_MPI
#ifdef HPCG_NO_LONG_LONG
  MPI_Allreduce(&localNumberOfNonzeros, &totalNumberOfNonzeros, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
#else
  long long lnnz = localNumberOfNonzeros, gnnz = 0;
  MPI_Allreduce(&lnnz, &gnnz, 1, MPI_LONG_LONG_INT, MPI_SUM, MPI_COMM_WORLD);
  totalNumberOfNonzeros = gnnz;
#endif
#else
  totalNumberOfNonzeros = localNumberOfNonzeros;
#endif

  assert(A.totalNumberOfRows == totalNumberOfRows);
  assert(A.totalNumberOfNonzeros == totalNumberOfNonzeros);
  assert(A.localNumberOfRows == localNumberOfRows);
  assert(A.localNumberOfNonzeros == localNumberOfNonzeros);
}
