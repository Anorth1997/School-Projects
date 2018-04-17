#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <stdlib.h>
// Add your other system includes here.

#include "ptree.h"

// Defining the constants described in ptree.h
const unsigned int MAX_PATH_LENGTH = 1024;

// If TEST is defined (see the Makefile), will look in the tests 
// directory for PIDs, instead of /proc.
#ifdef TEST
    const char *PROC_ROOT = "tests";
#else
    const char *PROC_ROOT = "/proc";
#endif


/* This function create a single TreeNode with only node->pid and node->name 
 * for the given process id.
 * a helper function for generate_ptree
 *
 * It returns 1 to repesent error. Specifically, cmdline file doesn't exist instead, 
 * it updates the contents pointed by node. If this pid is a valide process, node will 
 * points to a Treenode with pid and name, else it points to NULL. This function only take cares of 
 * assigning pid and name.
 */
int create_single_TreeNode(struct TreeNode **node, pid_t pid) {
    
    /*
     *  first of all, we want to check the existence of exe which
     *  implies that if it is a valid process
     *	if it exists, we can create a node with it
     */ 
      
    int error = 0;
    char procfile[MAX_PATH_LENGTH + 1];
    if (sprintf(procfile, "%s/%d/exe", PROC_ROOT, pid) < 0) {
        fprintf(stderr, "Step1: sprintf failed to produce a filename\n");
        *node = NULL;
        return 1;
    }


    struct stat exe_exist;
    if (lstat(procfile, &exe_exist) == 0) {
        *node = malloc(sizeof(struct TreeNode));
     
        (*node)->pid = pid; 
	(*node)->name = NULL;

        char proccmd[MAX_PATH_LENGTH + 1];
        if (sprintf(proccmd, "%s/%d/cmdline", PROC_ROOT, pid) < 0) {
            fprintf(stderr, "Step2, a: sprintf failed to produce the path for command line file\n");
            (*node)->name = NULL;
            return 1;
        }
   
        struct stat cmdline_exist;
        if (lstat(proccmd, &cmdline_exist) != 0) {
            fprintf(stderr, "Step2, a: cmdline path is invalid\n");
            (*node)->name = NULL;
            return 1;
	    
        } else {
            FILE *cmdline_file;

            
            cmdline_file = fopen(proccmd, "r");

            char store_cmdline[MAX_PATH_LENGTH + 1];
	    
            if (fgets(store_cmdline, MAX_PATH_LENGTH + 1, cmdline_file) == NULL) {
                fprintf(stderr, "Step 2, b: failed to read in store_cmdline, no contents in cmdline\n");
                (*node)->name = NULL;
                fclose(cmdline_file);
                return 0;
                
            } else {
                (*node)->name = malloc(sizeof(char) * strlen(store_cmdline) + 1);
            
             
                if (strcpy((*node)->name, store_cmdline) == NULL) {
                    fprintf(stderr, "failed to strcpy the store_cmdline to root->name\n");
                   
                    error = 1;
                }
		fclose(cmdline_file);
            }
        }
    } else {
        *node = NULL;
        return 1;
    }
    return error;
}


/*
 * Creates a PTree rooted at the process pid.
 * The function returns 0 if the tree was created successfully 
 * and 1 if the tree could not be created or if at least
 * one PID was encountered that could not be found or was not an 
 * executing process.
 */
int generate_ptree(struct TreeNode **root, pid_t pid) {

    int error = 0;

    
    error = create_single_TreeNode(root, pid);
    
    if (*root == NULL) {
        return 1;
    }
    

    char procchildren[MAX_PATH_LENGTH + 1];
    if (sprintf(procchildren, "%s/%d/task/%d/children", PROC_ROOT, pid, pid) < 0) {
        fprintf(stderr, "sprintf failed to setup the path for children file\n");
	return 1;
    }

    struct stat chidlren_exist;
    if (lstat(procchildren, &chidlren_exist) != 0) { 
        fprintf(stderr, "children path is invalid\n");
        (*root)->child = NULL;
        return 1;
    }


    FILE *children;
    children = fopen(procchildren, "r");
  
    pid_t child_pid;

    if (fscanf(children, "%d", &child_pid) != 1) {
        fclose(children);
        return error;
    }
    
    else {
        error = generate_ptree(&((*root)->child), child_pid);

        if ((*root)->child == NULL) {
            while (((*root)->child == NULL) && fscanf(children, "%d", &child_pid) == 1) {
                error = generate_ptree(&((*root)->child), child_pid);
            }         
            /* there are two conditions after finishing the above while loop. 
             * First, we finished reading through, and no valid children.
             * aka. root->child == NULL, then we just return error.
             * Second, we found a child for our root, and there are still some leftover 
             * children in our children file. We want to link them as siblings in next while loop. 
             */            
            if ((*root)->child == NULL) {
                fclose(children);
                return error;
            }
        }

        struct TreeNode *cur_child = (*root)->child;
        while (fscanf(children, "%d", &child_pid) == 1) {
	    struct TreeNode *next = NULL;
            error = generate_ptree(&next, child_pid);
            if (next != NULL) {
                cur_child->sibling = next;
                cur_child = next;
            }
        }
        fclose(children);
        return error;
    }
}


/*
 * Prints the TreeNodes encountered on a preorder traversal of an PTree
 * to a specified maximum depth. If the maximum depth is 0, then the 
 * entire tree is printed.
 */
void print_ptree(struct TreeNode *root, int max_depth) {
    // Here's a way to keep track of the depth (in the tree) you're at
    // and print 2 * that many spaces at the beginning of the line.
    static int depth = 0;
    /* base case: if current root is null
     */
    
    if (root != NULL) {
        if (root->name == NULL) {
            printf("%*s%d\n", depth * 2, "", root->pid);
        } else {
            printf("%*s%d: %s\n", depth * 2, "", root->pid, root->name);
        }

	/* If max_depth is 1, we iterate through its child and other nodes
	 * that linked to this child as siblings, and print all of them
	 */	
        if (max_depth == 1) {        
            struct TreeNode *cur_child = root->child;  
            depth++;
            while (cur_child != NULL) {
                if (cur_child->name == NULL) {
                    printf("%*s%d\n", depth * 2, "", cur_child->pid);
                } else {
                    printf("%*s%d: %s\n", depth * 2, "", cur_child->pid, cur_child->name);
                }
                cur_child = cur_child->sibling;
            }
            depth--;

        } 
	/* It max is not at depth 1, we go deeper to recusive through its child and 
	 * other nodes that linked to this child as siblings. the condition max_depth <= 0
	 * is designed for the case that when max_depth is 0, we print the entire tree
	 * Our base case will make sure this function to terminate.
	 */
	
	else if (max_depth > 1 || max_depth <= 0) {
            struct TreeNode *cur_child = root->child;
            if (cur_child != NULL) {
                depth++;
                while (cur_child != NULL) {
                    print_ptree(cur_child, max_depth - 1);
                    cur_child = cur_child->sibling; 
                }
                depth--; 
            }
        }
    }
}
