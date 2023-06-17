#include <iostream>
#include <vector>
#include <mpi.h>

using namespace std;

int main(int argc, char* argv[]) {
    const int n = 1000;
    vector<int> arr(n);
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int chunk_size = n / size;
    vector<int> local_arr(chunk_size);
    int local_max = 0;

    // Initialize the local array with values from the global array
    MPI_Scatter(&arr[0], chunk_size, MPI_INT, &local_arr[0], chunk_size, MPI_INT, 0, MPI_COMM_WORLD);

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
        cout << "Maximum value: " << max_val << endl;
    }

    MPI_Finalize();
    return 0;
}