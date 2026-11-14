
#include <immintrin.h>
#include <cmath>
#include <iomanip>
#include <iostream>

constexpr int N = 4;
constexpr double FAULT_DELTA = 100.0;

using Matrix = double[N][N];

// Inputs are kept separate from the computed matrices.
const Matrix A = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {2, 0, 1, 3},
    {4, 1, 2, 1}
};

const Matrix B = {
    {1, 0, 2, 1},
    {0, 1, 3, 2},
    {2, 1, 0, 3},
    {1, 2, 1, 0}
};

// Use the real CPU FMA instruction for arithmetic.
// Do not inline this function into main.
__attribute__((noinline))
void gemm_fma(Matrix& C, bool inject_fault) {

    for (int i = 0; i < N; ++i) {

        // One AVX register holds four doubles.
        __m256d acc = _mm256_setzero_pd();

        for (int k = 0; k < N; ++k) {

            // Broadcast one A value to all four lanes.
            __m256d a = _mm256_set1_pd(A[i][k]);

            // Load four B values.
            __m256d b = _mm256_loadu_pd(B[k]);

            // Four genuine FMA calculations.
            acc = _mm256_fmadd_pd(a, b, acc);

            // Simulate a fault in one arithmetic result.
            if (inject_fault && i == 1 && k == 2) {

                alignas(32) double lanes[4];

                // Read the intermediate FMA results.
                _mm256_storeu_pd(lanes, acc);

                double before = lanes[2];

                // Only one result is corrupted.
                lanes[2] += FAULT_DELTA;

                std::cout
                    << "FAULT INJECTED"
                    << " at row=" << i
                    << ", k=" << k
                    << ", lane=2"
                    << ", before=" << before
                    << ", after=" << lanes[2]
                    << "\n";

                // Put the faulty result back in the accumulator.
                acc = _mm256_loadu_pd(lanes);
            }
        }

        // Store the completed output row.
        _mm256_storeu_pd(C[i], acc);
    }
}

void print_matrix(const char* name, const Matrix& M) {
    std::cout << "\n" << name << "\n";

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            std::cout << std::setw(10) << M[i][j];
        }
        std::cout << "\n";
    }
}

int main() {
    Matrix baseline = {};
    Matrix faulty = {};

    std::cout << std::fixed << std::setprecision(2);

    // Run without error.
    gemm_fma(baseline, false);

    // Run with one controlled error.
    gemm_fma(faulty, true);

    print_matrix("BASELINE MATRIX:", baseline);
    print_matrix("FAULTY MATRIX:", faulty);

    std::cout << "\nDIFFERENCE MATRIX:\n";

    int changed = 0;
    double max_diff = 0.0;

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {

            double diff = faulty[i][j] - baseline[i][j];

            if (std::abs(diff) > 1e-9) {
                ++changed;
            }

            if (std::abs(diff) > max_diff) {
                max_diff = std::abs(diff);
            }

            std::cout << std::setw(10) << diff;
        }
        std::cout << "\n";
    }

    // Check independently calculated expected results.
    // The full correct matrix is:
    const Matrix expected = {
        {11, 13, 12, 14},
        {27, 29, 36, 38},
        {7, 7, 7, 5},
        {9, 5, 12, 12}
    };

    bool baseline_ok = true;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (std::abs(baseline[i][j] - expected[i][j])
                    > 1e-9) {
                baseline_ok = false;
            }
        }
    }

    bool fault_ok =
        changed == 1 &&
        std::abs(faulty[1][2] - baseline[1][2]
                 - FAULT_DELTA) < 1e-9;

    std::cout << "\nChanged elements: " << changed;
    std::cout << "\nMaximum difference: " << max_diff;
    std::cout << "\nBaseline check: "
              << (baseline_ok ? "PASS" : "FAIL");
    std::cout << "\nFault check: "
              << (fault_ok ? "PASS" : "FAIL")
              << "\n";

    return (baseline_ok && fault_ok) ? 0 : 1;
}
