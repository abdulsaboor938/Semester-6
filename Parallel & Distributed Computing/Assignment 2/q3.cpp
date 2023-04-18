#include <iostream>
#include <cmath>
#include <chrono>
// #include <omp.h>

double compute(double x) {
    double result = 0;
    for (int i = 0; i < 100000000; i++) {
        result += sin(x) * cos(x) * tan(x);
    }
    return result;
}

int main() {
    double x = 1.0;
    double result = 0;
    auto start_time = std::chrono::steady_clock::now();

#pragma omp parallel num_threads(4)
    {
#pragma omp sections nowait
        {
#pragma omp section
            {
                double temp1 = compute(x + 4);
#pragma omp critical
                result += temp1;
            }
#pragma omp section
            {
                double temp2 = compute(x + 5);
#pragma omp critical
                result += temp2;
            }
        }
#pragma omp barrier
#pragma omp sections nowait
        {
#pragma omp section
            {
                double temp3 = compute(x + 6);
#pragma omp critical
                result += temp3;
            }
#pragma omp section
            {
                double temp4 = compute(x + 7);
#pragma omp critical
                result += temp4;
            }
        }
#pragma omp barrier
#pragma omp sections nowait
        {
#pragma omp section
            {
                double temp5 = compute(x);
                double temp6 = compute(x + 1);
#pragma omp critical
                result += temp5 + temp6;
            }
#pragma omp section
            {
                double temp7 = compute(x + 2);
                double temp8 = compute(x + 3);
#pragma omp critical
                result += temp7 + temp8;
            }
        }
    }

    auto end_time = std::chrono::steady_clock::now();
    auto diff_time = end_time - start_time;
    std::cout << "Parallel computation took " << std::chrono::duration <double, std::milli> (diff_time).count() << " ms" << std::endl;

    std::cout << "Result: " << result << std::endl;

    return 0;
}
// int main() {
//     double x = 1.0;
//     double result = 0;

//     auto start_time = std::chrono::steady_clock::now();
//     result += compute(x + 4);
//     result += compute(x + 5);
//     result += compute(x + 6);
//     result += compute(x + 7);
//     double temp1 = compute(x);
//     double temp2 = compute(x + 1);
//     double temp3 = compute(x + 2);
//     double temp4 = compute(x + 3);
//     result += temp1 + temp2 + temp3 + temp4;
// }
