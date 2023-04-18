// OpenMp program to get total number of threads in parallel region

#include <iostream>
#include <omp.h>
using namespace std;

int main()
{
    #pragma omp parallel num_threads(4) // setting number of threads for parallel region
    {
        int num = omp_get_num_threads(); // to get maximum number of threads
        int id = omp_get_thread_num();
        cout << "Thread: "<<id<<" total threads: "<<num<<endl;
    }
    return 0;
}