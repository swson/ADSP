#ifndef READMTX_HPP
#define READMTX_HPP

#include "SparseMatrix.hpp"

/// Reads a Matrix Market (.mtx) file and initializes a SparseMatrix in HPCG format.
///
/// @param[in]  filename  Path to the .mtx file
/// @param[out] A         SparseMatrix to be filled (must be initialized with geometry)
///
/// @return true if successful, false otherwise
bool ReadMTX(const char* filename, SparseMatrix& A);

#endif // READMTX_HPP
