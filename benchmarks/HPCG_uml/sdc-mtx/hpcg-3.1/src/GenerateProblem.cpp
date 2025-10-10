
//@HEADER
// ***************************************************
//
// HPCG: High Performance Conjugate Gradient Benchmark
//
// Contact:
// Michael A. Heroux ( maherou@sandia.gov)
// Jack Dongarra     (dongarra@eecs.utk.edu)
// Piotr Luszczek    (luszczek@eecs.utk.edu)
//
// ***************************************************
//@HEADER

/*!
 @file GenerateProblem.cpp

 HPCG routine
 */

#ifndef HPCG_NO_MPI
#include <mpi.h>
#endif

#ifndef HPCG_NO_OPENMP
#include <omp.h>
#endif

#include <iostream>
#include <cstdlib>
#include <cstring>
#include "GenerateProblem.hpp"
#include "ReadMTX.hpp"
#include "SparseMatrix.hpp"
#include "Geometry.hpp"
#include "Vector.hpp"
#include "mytimer.hpp"

void GenerateProblem(SparseMatrix &A, Vector *b, Vector *x, Vector *xexact) {
  const char *mtx_path = getenv("HPCG_MATRIX_PATH");

  if (mtx_path) {
    std::cout << "[INFO] Using MTX file: " << mtx_path << std::endl;
    bool loaded = ReadMTX(mtx_path, A);
    if (!loaded) {
      std::cerr << "[ERROR] Failed to load MTX file. Exiting." << std::endl;
      std::exit(1);
    }

        A.geom = new Geometry();
    A.geom->nx = A.localNumberOfRows;
    A.geom->ny = 2;
    A.geom->nz = 2;
    A.geom->gnx = A.totalNumberOfRows;
    A.geom->gny = 1;
    A.geom->gnz = 1;
    A.geom->npx = 1;
    A.geom->npy = 1;
    A.geom->npz = 1;
    A.geom->size = 1;
    A.geom->rank = 0;
    A.geom->numThreads = 1;
    A.geom->pz = 0;
    
  } else {
    std::cerr << "[ERROR] No MTX file provided (HPCG_MATRIX_PATH not set). Exiting." << std::endl;
    std::exit(1);
  }

  if (b) {
    InitializeVector(*b, A.localNumberOfRows);
    for (local_int_t i = 0; i < b->localLength; ++i)
      b->values[i] = 26.0 - (double)(A.nonzerosInRow[i] - 1); // 근사값
  }

  if (x) {
    InitializeVector(*x, A.localNumberOfRows);
    std::fill(x->values.begin(), x->values.end(), 0.0);
  }

  if (xexact) {
    InitializeVector(*xexact, A.localNumberOfRows);
    std::fill(xexact->values.begin(), xexact->values.end(), 1.0);
  }
}
