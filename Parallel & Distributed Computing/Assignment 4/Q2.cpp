#include <iostream>
#include <vector>
#include <mpi.h>
#include <omp.h>

using namespace std;

int main()
{
    // initializing matrix
    int m = 4, n = 4;
    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++)
        {
            matrix[i][j] = rand() % 100;
        }
    }

    // initializing MPI
    int rank, size;
    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // initializing OpenMP
    int num_threads = 4;
    omp_set_num_threads(num_threads);   

    // distributing rows to processes
    int chunk_size = m / size;
    vector<int> local_arr(chunk_size);
    MPI_Scatter(&matrix[0], chunk_size, MPI_INT, &local_arr[0], chunk_size, MPI_INT, 0, MPI_COMM_WORLD);

    // sorting rows using merge sort
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
        int chunk_size = m / num_threads;
        int start = tid * chunk_size;
        int end = start + chunk_size;
        if (tid == num_threads - 1) {
            end = m;
        }
        for (int i = start; i < end; i++) {
            for (int j = i + 1; j < end; j++) {
                if (local_arr[i] < local_arr[j]) {
                    int temp = local_arr[i];
                    local_arr[i] = local_arr[j];
                    local_arr[j] = temp;
                }
            }
        }
    }

    // computing sum of rows
    int local_sum = 0;
    for (int i = 0; i < chunk_size; i++) {
        local_sum += local_arr[i];
    }

    // gathering sorted rows
    if (rank != 0) {
        MPI_Send(&local_arr[0], chunk_size, MPI_INT, 0, 0, MPI_COMM_WORLD);
    } else {
        vector<int> sorted_matrix(m);
        for (int i = 0; i < chunk_size; i++) {
            sorted_matrix[i] = local_arr[i];
        }
        for (int i = 1; i < size; i++) {
            MPI_Recv(&sorted_matrix[i * chunk_size], chunk_size, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        cout << "Sorted matrix: " << endl;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                cout << sorted_matrix[i][j] << " ";
            }
            cout << endl;
        }
    }

    // computing sum of matrix
    int sum = 0;
    MPI_Reduce(&local_sum, &sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    if (rank == 0) {
        cout << "Sum of matrix: " << sum << endl;
    }

    MPI_Finalize();
    return 0;
}