#include "ReadMTX.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_set>
#include <iomanip>


bool ReadMTX(const char* filename, SparseMatrix & A) {
  std::ifstream infile(filename);
  if (!infile) {
    std::cerr << "[ERROR] Cannot open MTX file: " << filename << std::endl;
    return false;
  }

  std::string line;
  while (std::getline(infile, line)) {
    if (line[0] != '%') break;
  }

  std::istringstream iss(line);
  local_int_t rows, cols, nnz;
  iss >> rows >> cols >> nnz;

  A.localNumberOfRows = rows;
  A.localNumberOfColumns = cols;
  A.localNumberOfNonzeros = nnz;
  A.totalNumberOfRows = rows;
  A.totalNumberOfNonzeros = nnz;

  A.nonzerosInRow.resize(rows, 0);
  A.matrixValues.resize(rows);
  A.matrixDiagonal.resize(rows, nullptr);
  A.mtxIndG.resize(rows);
  A.mtxIndL.resize(rows);
  A.localToGlobalMap.resize(rows);
  A.globalToLocalMap.clear();

  for (int i = 0; i < nnz; ++i) {
    local_int_t r, c;
    double val;
    infile >> r >> c >> val;
    r--; c--; // Convert from 1-based to 0-based

    A.matrixValues[r].push_back(val);
    A.mtxIndG[r].push_back(c);
    A.mtxIndL[r].push_back(c);
    A.nonzerosInRow[r]++;
  }

  // Build diagonal and local-global maps
  for (int i = 0; i < rows; ++i) {
    A.localToGlobalMap[i] = i;
    A.globalToLocalMap[i] = i;

    bool foundDiag = false;
    for (size_t j = 0; j < A.mtxIndG[i].size(); ++j) {
      if (A.mtxIndG[i][j] == i) {
        A.matrixDiagonal[i] = &A.matrixValues[i][j];
        foundDiag = true;
        break;
      }
    }

    if (!foundDiag) {
      A.matrixValues[i].push_back(1.0);
      A.mtxIndG[i].push_back(i);
      A.mtxIndL[i].push_back(i);
      A.matrixDiagonal[i] = &A.matrixValues[i].back();
      A.nonzerosInRow[i]++;
      A.localNumberOfNonzeros++;
      A.totalNumberOfNonzeros++;
    }
  }
  std::ofstream csv("debug_sparse_matrix.csv");
  csv << "row,col,value" << std::endl;
  for (int i = 0; i < rows; ++i) {
    for (size_t j = 0; j < A.mtxIndG[i].size(); ++j) {
      csv << i << "," << A.mtxIndG[i][j] << "," << std::setprecision(12) << A.matrixValues[i][j] << std::endl;
    }
  }
  csv.close();

  return true;
}
