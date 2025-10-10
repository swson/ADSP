#ifndef SPARSEMATRIX_HPP
#define SPARSEMATRIX_HPP

#include <vector>
#include <set>
#include <unordered_map>
#include <random>
#include <cassert>
#include "Geometry.hpp"
#include "Vector.hpp"
#include "MGData.hpp"
#include <iostream>
#include <unordered_set>

using GlobalToLocalMap = std::unordered_map<global_int_t, local_int_t>;

struct SparseMatrix_STRUCT {
  char *title;
  Geometry *geom;

  global_int_t totalNumberOfRows;
  global_int_t totalNumberOfNonzeros;

  local_int_t localNumberOfRows;
  local_int_t localNumberOfColumns;
  local_int_t localNumberOfNonzeros;

  std::vector<char> nonzerosInRow;
  std::vector<std::vector<global_int_t>> mtxIndG;
  std::vector<std::vector<local_int_t>> mtxIndL;
  std::vector<std::vector<double>> matrixValues;
  std::vector<double*> matrixDiagonal;

  GlobalToLocalMap globalToLocalMap;
  std::vector<global_int_t> localToGlobalMap;

  mutable SparseMatrix_STRUCT *Ac;
  mutable MGData *mgData;
  void *optimizationData;

  mutable bool isDotProductOptimized;
  mutable bool isSpmvOptimized;
  mutable bool isMgOptimized;
  mutable bool isWaxpbyOptimized;

#ifndef HPCG_NO_MPI
  local_int_t numberOfExternalValues;
  int numberOfSendNeighbors;
  local_int_t totalToBeSent;
  local_int_t *elementsToSend;
  int *neighbors;
  local_int_t *receiveLength;
  local_int_t *sendLength;
  double *sendBuffer;
#endif

  void inject_errors(double err_rate, double inj_rate) {
    std::random_device rd;
    std::mt19937 gen(rd());

    if (localNumberOfRows == 0 || localNumberOfNonzeros == 0) {
      std::cerr << "[ERROR] Empty matrix — cannot inject errors.\n";
      return;
    }

    int n = static_cast<int>(localNumberOfNonzeros * inj_rate);
    std::vector<std::set<int>> selected(localNumberOfRows);
    std::uniform_int_distribution<int> row_dist(0, localNumberOfRows - 1);

    int attempts = 0, max_attempts = 10 * n;
    int injected_targets = 0;

    while (injected_targets < n && attempts < max_attempts) {
      int r = row_dist(gen);

      // Skip empty rows
      if (nonzerosInRow[r] == 0 || matrixValues[r].empty()) {
	attempts++;
	continue;
      }

      // Avoid injecting more than available entries
      if (selected[r].size() >= matrixValues[r].size()) {
	attempts++;
	continue;
      }

      std::uniform_int_distribution<int> col_dist(0, nonzerosInRow[r] - 1);
      int c = col_dist(gen);

      // Retry if already selected
      if (selected[r].count(c)) {
	attempts++;
	continue;
      }

      selected[r].insert(c);
      injected_targets++;
    }

    if (attempts >= max_attempts) {
      std::cerr << "[WARN] inject_errors(): Reached max attempts, injected only "
		<< injected_targets << "/" << n << " targets.\n";
    }

    // Now apply the error
    for (int i = 0; i < localNumberOfRows; ++i) {
      for (int j : selected[i]) {
	std::normal_distribution<double> gauss(0, err_rate);
	double noise = gauss(gen);
	matrixValues[i][j] += noise;

	std::cout << "[DEBUG] Error injected at (" << i << "," << j << "): "
		  << "noise=" << noise << ", new_value=" << matrixValues[i][j] << "\n";
      }
    }

    std::cout << "[INFO] Total error injections: " << injected_targets << std::endl;
  }

};

typedef struct SparseMatrix_STRUCT SparseMatrix;

inline void InitializeSparseMatrix(SparseMatrix &A, Geometry *geom) {
  A.title = nullptr;
  A.geom = geom;
  A.totalNumberOfRows = 0;
  A.totalNumberOfNonzeros = 0;
  A.localNumberOfRows = 0;
  A.localNumberOfColumns = 0;
  A.localNumberOfNonzeros = 0;

  A.nonzerosInRow.clear();
  A.mtxIndG.clear();
  A.mtxIndL.clear();
  A.matrixValues.clear();
  A.matrixDiagonal.clear();

  A.isDotProductOptimized = true;
  A.isSpmvOptimized = true;
  A.isMgOptimized = true;
  A.isWaxpbyOptimized = true;

#ifndef HPCG_NO_MPI
  A.numberOfExternalValues = 0;
  A.numberOfSendNeighbors = 0;
  A.totalToBeSent = 0;
  A.elementsToSend = nullptr;
  A.neighbors = nullptr;
  A.receiveLength = nullptr;
  A.sendLength = nullptr;
  A.sendBuffer = nullptr;
#endif

  A.Ac = nullptr;
  A.mgData = nullptr;
}

inline void CopyMatrixDiagonal(SparseMatrix &A, Vector &diagonal) {
  assert(A.localNumberOfRows == diagonal.localLength);
  for (local_int_t i = 0; i < A.localNumberOfRows; ++i)
    diagonal.values[i] = *(A.matrixDiagonal[i]);
}

inline void ReplaceMatrixDiagonal(SparseMatrix &A, Vector &diagonal) {
  assert(A.localNumberOfRows == diagonal.localLength);
  for (local_int_t i = 0; i < A.localNumberOfRows; ++i)
    *(A.matrixDiagonal[i]) = diagonal.values[i];
}

inline void DeleteMatrix(SparseMatrix & A) {
  // STL vector 기반이므로 delete[] 대신 .clear() 사용
  A.matrixValues.clear();
  A.matrixDiagonal.clear();
  A.mtxIndG.clear();
  A.mtxIndL.clear();
  A.nonzerosInRow.clear();
  A.localToGlobalMap.clear();
  A.globalToLocalMap.clear();

#ifndef HPCG_NO_MPI
  A.elementsToSend.clear();
  A.neighbors.clear();
  A.receiveLength.clear();
  A.sendLength.clear();
  A.sendBuffer.clear();
#endif

  if (A.geom)    { DeleteGeometry(*A.geom); delete A.geom; A.geom = nullptr; }
  if (A.Ac)      { DeleteMatrix(*A.Ac); delete A.Ac; A.Ac = nullptr; }
  if (A.mgData)  { DeleteMGData(*A.mgData); delete A.mgData; A.mgData = nullptr; }
}

#endif // SPARSEMATRIX_HPP
