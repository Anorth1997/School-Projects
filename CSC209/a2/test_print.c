#include <stdio.h>
#include <stdlib.h>

#include "ptree.h"


int main(int argc, char *argv[]) {
    // Creates a ptree to test printing
    // Notice that in this tree the names are string literals. This is fine for
    // testing but is not what the assignment asks you to do in generate_ptree.
    // Read the handout carefully. 
    struct TreeNode root, child_one, child_two, grandchild;
    root.pid = 4511;
    root.name = "root process";
    root.child = &child_one;
    root.sibling = NULL;

    child_one.pid = 4523;
    child_one.name = "first child";
    child_one.child = &grandchild;
    child_one.sibling = &child_two;

    child_two.pid = 4524; 
    child_two.name = "second child";
    child_two.child = NULL;
    child_two.sibling = NULL;

    grandchild.pid = 4609;
    grandchild.name = "grandchild";
    grandchild.child = NULL;
    grandchild.sibling = NULL;

    print_ptree(&root, 0);
    print_ptree(&root, 1);
    print_ptree(&root, 2);
    print_ptree(&root, 3);

    return 0;
}

