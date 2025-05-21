#ifndef VECTOR_HPP
#define VECTOR_HPP

#include <vector>
#include <cstdlib>
#include <cassert>
#include "Geometry.hpp"

struct Vector_STRUCT {
  local_int_t localLength;
  std::vector<double> values;
  void *optimizationData;
};

typedef struct Vector_STRUCT Vector;

inline void InitializeVector(Vector &v, local_int_t localLength) {
  v.localLength = localLength;
  v.values.resize(localLength, 0.0);
  v.optimizationData = nullptr;
}

inline void ZeroVector(Vector &v) {
  std::fill(v.values.begin(), v.values.end(), 0.0);
}

inline void ScaleVectorValue(Vector &v, local_int_t index, double value) {
  assert(index >= 0 && index < v.localLength);
  v.values[index] *= value;
}

inline void FillRandomVector(Vector &v) {
  for (auto &val : v.values)
    val = rand() / (double)RAND_MAX + 1.0;
}

inline void CopyVector(const Vector &v, Vector &w) {
  assert(v.localLength == w.localLength);
  w.values = v.values;
}

inline void DeleteVector(Vector &v) {
  v.values.clear();
  v.localLength = 0;
}
#endif // VECTOR_HPP
