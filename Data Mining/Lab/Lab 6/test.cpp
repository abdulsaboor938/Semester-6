#include <iostream>
#include <random>
#include <chrono>
#include <omp.h>

// Node structure for the binary tree
struct Node {
    int value;
    Node* left;
    Node* right;
    Node(int value) : value(value), left(nullptr), right(nullptr) {}
};

// Function to insert a new node into the binary tree
void insertNode(Node*& node, int value) {
    if (node == nullptr) {
        node = new Node(value);
    } else if (value < node->value) {
        insertNode(node->left, value);
    } else if (value > node->value) {
        insertNode(node->right, value);
    }
}

// Function to search for a value in the binary tree
bool searchNode(Node* node, int value) {
    if (node == nullptr) {
        return false;
    } else if (value == node->value) {
        return true;
    } else if (value < node->value) {
        return searchNode(node->left, value);
    } else {
        return searchNode(node->right, value);
    }
}

int main() {
    // Set the number of nodes in the binary tree
    const int numNodes = 30;

    // Initialize the random number generator
    std::default_random_engine generator(std::chrono::system_clock::now().time_since_epoch().count());
    std::uniform_int_distribution<int> distribution(1, 100);

    // Create the binary tree with random integer values
    Node* root = nullptr;
    #pragma omp parallel for
    for (int i = 0; i < numNodes; i++) {
        int value = distribution(generator);
        #pragma omp critical
        {
            insertNode(root, value);
        }
    }

    // Search for a value in the binary tree
    int searchValue = distribution(generator);
    bool found = searchNode(root, searchValue);
    if (found) {
        std::cout << "Found " << searchValue << " in the binary tree." << std::endl;
    } else {
        std::cout << "Did not find " << searchValue << " in the binary tree." << std::endl;
    }

    // Free the memory used by the binary tree
    // ...
    return 0;
}


// change the following code to use OpenMP
// Path: test.cpp
#include <iostream>
#include <random>
#include <chrono>
#include <omp.h>
 
// Node structure for the binary tree
struct Node {
    int value;
    Node* left;
    Node* right;
    Node(int value) : value(value), left(nullptr), right(nullptr) {}
};

// Function to insert a new node into the binary tree
void insertNode(Node*& node, int value) {
    if (node == nullptr) {
        node = new Node(value);
    } else if (value < node->value) {
        insertNode(node->left, value);
    } else if (value > node->value) {
        insertNode(node->right, value);
    }
}

// Function to search for a value in the binary tree
bool searchNode(Node* node, int value) {
    if (node == nullptr) {
        return false;
    } else if (value == node->value) {
        return true;
    } else if (value < node->value) {
        return searchNode(node->left, value);
    } else {
        return searchNode(node->right, value);
    }
}

int main() {
    // Set the number of nodes in the binary tree
    const int numNodes = 30;

    // Initialize the random number generator
    std::default_random_engine generator(std::chrono::system_clock::now().time_since_epoch().count());
    std::uniform_int_distribution<int> distribution(1, 100);

    // Create the binary tree with random integer values
    Node* root = nullptr;
    #pragma omp parallel for
    for (int i = 0; i < numNodes; i++) {
        int value = distribution(generator);
        #pragma omp critical
        {
            insertNode(root, value);
        }
    }

    // Search for a value in the binary tree
    int searchValue = distribution(generator);
    bool found = searchNode(root, searchValue);
    if (found) {
        std::cout << "Found " << searchValue << " in the binary tree." << std::endl;
    } else {
        std::cout << "Did not find " << searchValue << " in the binary tree." << std::endl;
    }

    // Free the memory used by the binary tree
    // ...
    return 0;
}


