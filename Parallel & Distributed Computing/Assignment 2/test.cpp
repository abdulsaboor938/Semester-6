// Write C/C++ code using OpenMP to create a binary tree with random integer values using
// the random value function and implement the functionality to search for any value from the
// binary tree. There should be a minimum of thirty nodes for the tree that you test your
// program with. You can use the random function to fill the binary tree.

#include <iostream>
#include <cstdlib>
#include <ctime>
// #include <omp.h>
using namespace std;

struct node
{
    int data;
    node *left;
    node *right;
};

node *root = NULL;

void insert(int data)
{
    node *temp = new node;
    temp->data = data;
    temp->left = NULL;
    temp->right = NULL;
    if (root == NULL)
    {
        root = temp;
    }
    else
    {
        node *current = root;
        node *parent = NULL;
        while (true)
        {
            parent = current;
            if (data < current->data)
            {
                current = current->left;
                if (current == NULL)
                {
                    parent->left = temp;
                    return;
                }
            }
            else
            {
                current = current->right;
                if (current == NULL)
                {
                    parent->right = temp;
                    return;
                }
            }
        }
    }
}

void search(int data)
{
    node *current = root;
    while (current != NULL)
    {
        if (current->data == data)
        {
            cout << "Found " << data << endl;
            return;
        }
        else if (current->data > data)
        {
            current = current->left;
        }
        else
        {
            current = current->right;
        }
    }
    cout << "Not found " << data << endl;
}

int main()
{
    srand(time(NULL));
    int n = 30;
    int *arr = new int[n];
    for (int i = 0; i < n; i++)
    {
        arr[i] = rand() % 100;
        insert(arr[i]);
    }
    
    // print the tree
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << ", ";
    }
    return 0;
}