#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char* argv[]) {
    const int n = 1000;
    int *arr = (int*) malloc(n * sizeof(int));
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int chunk_size = n / size;
    int *local_arr = (int*) malloc(chunk_size * sizeof(int));
    int local_max = 0;

    // Initialize the local array with values from the global array
    MPI_Scatter(arr, chunk_size, MPI_INT, local_arr, chunk_size, MPI_INT, 0, MPI_COMM_WORLD);

    // Find the maximum value in the local array
    for (int i = 0; i < chunk_size; i++) {
        if (local_arr[i] > local_max) {
            local_max = local_arr[i];
        }
    }

    // Send the local maximum value to the root process
    if (rank != 0) {
        MPI_Send(&local_max, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    } else {
        int max_val = local_max;
        for (int i = 1; i < size; i++) {
            int recv_max;
            MPI_Recv(&recv_max, 1, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (recv_max > max_val) {
                max_val = recv_max;
            }
        }
        printf("Maximum value: %d\n", max_val);
    }

    MPI_Finalize();
    free(arr);
    free(local_arr);
    return 0;
}
