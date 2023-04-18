// this is a fle to simulate the hello world program and give a description of all teh functions being used

#include <mpi.h> // this is the header file that needs to be included for using the mpi functions in the program
#include <iostream>

using namespace std;

int main()
{
    // the mpi works normally inside the main function

    MPI_Init(NULL, NULL); // this function is used to initialize the mpi environment
    // MPI_Init(int *argc, char ***argv) // this is the function prototype, but for simplicity we will pass NULL 

    // Communicator is a group of processes that can communicate with each other
    // MPI_COMM_WORLD is the default communicator that is used by all the processes
    // this can be stored in MPI_Comm variable
    MPI_Comm comm = MPI_COMM_WORLD;

    // MPI_Comm_size is used to get the number of processes in the communication domain
    // MPI_Comm_size(MPI_Comm comm, int *size) is the function prototype
    int size = 0;
    MPI_Comm_size(comm, &size);
    cout<<"The size of communication domain is: "<<size<<endl;

    // MPI_Comm_rank is used to get the rank of the process in communication domain
    // MPI_Comm_rank(MPI_Comm comm, int *rank) is the function prototype
    int rank = 0;
    MPI_Comm_rank(comm, &rank);
    cout<<"The rank of the process is: "<<rank<<endl;
    // keep in mind that the rank of the process is always between 0 and size-1
    // and the rank of parent process is always assumed to be 0

    // MPI_Finalize is used to finalize the mpi environment
    // MPI_Finalize() is the function prototype
    MPI_Finalize();

    // send message if the rank is 0
    if(rank == 0)
    {
        // here we will try to send the message to the process with rank 1
        // MPI_Send(void *buf, int count, MPI_Datatype datatype, int dest, int tag, MPI_Comm comm) is the prototype
        // buf is the pointer to the buffer that contains the data to be sent
        // count is the number of elements in the buffer
        // datatype is the datatype of the elements in the buffer
        // dest is the rank of the destination process
        // tag is the message tag, should be unique for each message and same in both the processes
        // comm is the communicator
        // MPI_Send is a blocking function, it will block the process until the message is sent

        int data = 10;
        MPI_Send(&data, 1, MPI_INT, 1, 0, comm);
    }

    // receive message if the rank is 1
    if (rank == 1)
    {
        // here we will try to receive the message from the process with rank 0
        // MPI_Recv(void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Status *status) is the prototype
        // buf is the pointer to the buffer that will contain the data to be received
        // count is the number of elements in the buffer
        // datatype is the datatype of the elements in the buffer
        // source is the rank of the source process
        // tag is the message tag, should be unique for each message and same in both the processes
        // comm is the communicator
        // status is the status object that will contain the status of the message
        // MPI_Recv is a blocking function, it will block the process until the message is received

        int data = 0;
        MPI_Recv(&data, 1, MPI_INT, 0, 0, comm, MPI_STATUS_IGNORE);
        cout<<"The data received is: "<<data<<endl;
    }

    // an example of MPI_Sendrecv
    // MPI_Sendrecv(void *sendbuf, int sendcount, MPI_Datatype sendtype, int dest, int sendtag, void *recvbuf, int recvcount, MPI_Datatype recvtype, int source, int recvtag, MPI_Comm comm, MPI_Status *status) is the prototype
    // sendbuf is the pointer to the buffer that contains the data to be sent
    // sendcount is the number of elements in the buffer
    // sendtype is the datatype of the elements in the buffer
    // dest is the rank of the destination process
    // sendtag is the message tag, should be unique for each message and same in both the processes
    // recvbuf is the pointer to the buffer that will contain the data to be received
    // recvcount is the number of elements in the buffer
    // recvtype is the datatype of the elements in the buffer
    // source is the rank of the source process
    // recvtag is the message tag, should be unique for each message and same in both the processes
    // comm is the communicator
    // status is the status object that will contain the status of the message
    // MPI_Sendrecv is a blocking function, it will block the process until the message is sent and received

    int data = 0;
    if(rank == 0)
    {
        data = 10;
        MPI_Sendrecv(&data, 1, MPI_INT, 1, 0, &data, 1, MPI_INT, 1, 0, comm, MPI_STATUS_IGNORE);
        cout<<"The data received is: "<<data<<endl;
    }
    if(rank == 1)
    {
        data = 20;
        MPI_Sendrecv(&data, 1, MPI_INT, 0, 0, &data, 1, MPI_INT, 0, 0, comm, MPI_STATUS_IGNORE);
        cout<<"The data received is: "<<data<<endl;
    }

    // Suppose we don't know the lenghth of receiving buffer, then we can use MPI_Probe followed by MPI_Get_count
    // MPI_Probe(int source, int tag, MPI_Comm comm, MPI_Status *status) is the prototype
    // MPI_Get_count(MPI_Status *status, MPI_Datatype datatype, int *count) is the prototype

    // now to some collective communication
    // MPI_Bcast(void *buffer, int count, MPI_Datatype datatype, int root, MPI_Comm comm) is the prototype
    // buffer is the pointer to the buffer that contains the data to be sent or will contain the data to be received
    // count is the number of elements in the buffer
    // datatype is the datatype of the elements in the buffer
    // root is the rank of the root process
    // comm is the communicator
    // MPI_Bcast is a blocking function, it will block the process until the message is sent or received
    if (rank == 0)
    {
        data = 10;
    }
    MPI_Bcast(&data, 1, MPI_INT, 0, comm);
    cout<<"The data received is: "<<data<<endl;

    // MPI_Reduce(void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype, MPI_Op op, int root, MPI_Comm comm) is the prototype
}