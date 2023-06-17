// THis file is the description of working of the OpenMp

#include<iostream>
#include<omp.h>

using namespace std;

int main()
{
    // openmp uses the pragma directive to parallelize the code
    // we need to define the number of threads to be used, which can be done in two ways
    
    omp_set_num_threads(4); // this is the function to set the number of threads

    // or in the pragma directive itself
    #pragma omp parallel num_threads(4)
    {
        // this is the parallel region of this code
    }

    // now moving on to the for loop construct
    // This can be done in three ways

    // Naive, normal for loop
    for(int i=0;i<10;i++)
    {
        // do something
    }

    // omp parallel region
    int N=10;
    #pragma omp parallel num_threads(4)
    {
        int i, id, start, end, nthreads;
        id = omp_get_thread_num(); // This function returns the thread id, 0 is the master thread
        nthreads = omp_get_num_threads(); // This function returns the total number of working threads, keep in mind that this can be different than the number of threads defined in the omp_set_num_threads() function
        start = id*N/nthreads; // This is the starting index of the thread
        end = (id+1)*N/nthreads; // This is the ending index of the thread
        for(i=start;i<end;i++)
        {
            // do something
        }
    }

    // omp for construct
    #pragma omp parallel
    {
        int N=10;
        #pragma omp for
        for(int i=0;i<N;i++)
        {
            // do something
        }
    }

    // ------------------------------------------------------------------------------------

    // omp critical construct
    // This construct is used to make sure that only one thread can access the critical section at a time
    // most likely this is used to update a shared variable, inside a loop
    omp critical
    {
        // do something
    }

    // ------------------------------------------------------------------------------------

    // omp scheduling

    // static scheduling
    // In this scheduling, the iterations are divided into equal chunks and are assigned to the threads
    // This is the default scheduling
    #pragma omp for schedule(static)
    #pragma omp for schedule(static, 2) // this is the chunk size, by default it is 1

    // dynamic scheduling
    #pragma omp for schedule(dynamic, 2) // this is the chunk size, by default it is 1
    #pragma omp for schedule(dynamic) // this is the chunk size, by default it is 1

    // ------------------------------------------------------------------------------------

    // omp reduction
    // This is used to update a shared variable, by using the private copy of the variable for each thread
    // and then updating the shared variable at the end of the parallel region
    int sum=0;
    #pragma omp parallel for reduction(+:sum)
    for(int i=0;i<10;i++)
    {
        sum += i;
    }

    // ------------------------------------------------------------------------------------

    // omp atomic
    // This is used to update a shared variable, by using the private copy of the variable for each thread
    // and then updating the shared variable at the end of the parallel region
    int sum=0;
    #pragma omp parallel for
    for(int i=0;i<10;i++)
    {
        #pragma omp atomic
        sum += i;
    }

    #pragma omp atomic update
    sum += 1; // this is the same as the above code, updated automatically

    #pragma omp atomic read
    temp = sum; // temp is the private copy of the sum variable

    #pragma omp atomic write
    sum = n*m; // sum is updated without conflicts from other threads

    #pragma omp atomic catpure
    temp = ++sum; // increment and then capture the value of sum

    #pragma omp atomic capture
    {
        temp = sum; // capture the value of sum
        sum = 0; // reset the value of sum
    }
}

// ------------------------------------------------------------------------------------
// omp parallel sections
// This is used to divide the code into sections, which can be executed in parallel
// This is used when the code is not a loop, but a set of instructions

int main()
{
    #pragma omp parallel sections shared(a,b,c) private(x,y,z) // the variables can be defined before section begins, shared can be common for all while private ones have a separate copy for each thread
    {
        #pragma omp section
        {
            // do something
        }

        #pragma omp section
        {
            // do something
        }
    }
}

// ------------------------------------------------------------------------------------
// omp sections
// This is used to divide the code into sections, which can be executed in parallel
// The main difference here is that it uses existing threads rather than creating new ones

int main()
{
    // variables
    #pragma omp parallel num_threads(2)
    {
        // keep in mind that this should appear inside a parallel block and not outside
        #pragma omp sections
        {
            #pragma omp section
            {
                // do something
            }

            #pragma omp section
            {
                // do something
            }
        }
        #pragma omp sections
        {
            #pragma omp section
            {
                // do something
            }

            #pragma omp section
            {
                // do something
            }
        }
    }
}

// ------------------------------------------------------------------------------------
// omp single
// This is used to execute a block of code by a single thread, which is not the master thread

int main()
{
    #pragma omp parallel num_threads(4)
    {
        #pragma omp single
        {
            // do something
        }
    }
}

// ------------------------------------------------------------------------------------
// omp barrier
// This is used to make sure that all the threads have reached a certain point in the code
// This is used to synchronize the threads

int main()
{
    #pragma omp parallel num_threads(4)
    {
        // do something
        #pragma omp barrier
        // do something
    }
}

// ------------------------------------------------------------------------------------
// omp no wait
// This is used to make sure that all the threads have reached a certain point in the code
// This is used to synchronize the threads

int main()
{
    #pragma omp parallel num_threads(4)
    {
        // do something
        #pragma omp for nowait
        // do something
    }
}

// ------------------------------------------------------------------------------------
// omp lock
// This is to synchronize the threads, by locking the critical section
// This is used to make sure that only one thread can access the critical section at a time

int main()
{
    omp_lock_t lock;
    omp_init_lock(&lock); // this is to initialize the lock

    #pragma omp parallel num_threads(4)
    {
        // do something
        omp_set_lock(&lock); // this is to lock the critical section
        // do something
        omp_unset_lock(&lock); // this is to unlock the critical section
    }

    omp_destroy_lock(&lock); // this is to destroy the lock
}