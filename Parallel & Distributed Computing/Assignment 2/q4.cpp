#include <iostream>
#include <cstdlib>
#include <ctime>
// #include <omp.h>
using namespace std;

//node in a binary tree
struct TreeNode 
{
    int value;
    TreeNode* left;
    TreeNode* right;
};

// Function to create a new node
TreeNode* newNode(int value)
{
    TreeNode* node = new TreeNode();
    node->value = value;
    node->left = node->right = NULL;
    return node;
}

// Function to insert a new node in the binary tree
void insertNode(TreeNode*& root, int value)
{
    if (root == NULL) {
        root = newNode(value);
    }
    else if (value <= root->value) {
        insertNode(root->left, value);
    }
    else {
        insertNode(root->right, value);
    }
}

// Function to search for a value in the binary tree
bool searchValue(TreeNode* root, int value)
{
    if (root == NULL) {
        return false;
    }
    else if (root->value == value) {
        return true;
    }
    else if (value <= root->value) {
        return searchValue(root->left, value);
    }
    else {
        return searchValue(root->right, value);
    }
}

// In-order traversal to print the values of the nodes in the binary tree
void inOrderTraversal(TreeNode* root)
{
    if (root != NULL) {
        inOrderTraversal(root->left);
        cout << root->value << " ";
        inOrderTraversal(root->right);
    }
}

int main()
{
    // Seed the random number generator
    srand(time(NULL));
    // srand(2); // for not finding value
    // srand(9); // for finding value

    int num_nodes = 30;
    int val = 100;

    // Create the binary tree with random values
    TreeNode* root = NULL;
    #pragma omp parallel for num_threads(4)

    for (int i = 0; i < num_nodes; i++) 
    {
        int value = rand() %val + 1;
        #pragma omp critical
        //used by 1 thread at a time
        {
            insertNode(root, value);
        }
    }

    // Print the values of the nodes in the binary tree
    cout << "Values in the binary tree: ";
    inOrderTraversal(root);
    cout << endl;

    // Search for a value in the binary tree
    int find_val = rand() % val + 1;
    cout << "\nSearching for " << find_val << " in the tree: " << endl;
    
    bool found = searchValue(root, find_val);
    if (found) 
    {
        cout <<  find_val << " found in the tree" << endl;
    }
    else {
        cout <<  find_val << " not found the tree" << endl;
    }

    return 0;

    // print current time
    // auto end_time = std::chrono::steady_clock::now();
    
}
