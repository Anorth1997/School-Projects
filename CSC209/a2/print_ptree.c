#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ptree.h"

/* This main function can take 2 arguments or 4 arguments, corresponds to without 
 * optional flag -d or with optional flag -d. The first if condition handles the 
 * case that without optional flag, the else if condition handles the case that
 * with optional flag. 
 *
 * the number value followed by optional flag -d represents the max_depth to print.
 *  
 * This function returns 2 if there is some error during building the tree,
 * returns 1 if the user give the wrong arguments. returns 0 if everything succeed.
 */

int main(int argc, char **argv) {    
    

    if (argc != 2 && argc != 4) {
        fprintf(stderr, "first step: number of arguments wrong: Usage:\\n\\tptree [-d N] PID\n");
        return 1;
    } 
    
    int error = 0;
    struct TreeNode *root = NULL;
    
    if (argc == 2) { 

        error = generate_ptree(&root, strtol(argv[1], NULL, 10));
        print_ptree(root, 0);
	
        if (error != 0) {
            return 2;
        } else {
            return 0;
        }
    } else if (argc == 4) {
        if ((strlen(argv[1]) != 2) || argv[1][0] != '-' || argv[1][1] != 'd') {
            fprintf(stderr, "arguments wrong: Usage:\\n\\tptree [-d N] PID\n");
            return 1;
        } 
        
        error = generate_ptree(&root, strtol(argv[3], NULL, 10));
        print_ptree(root, strtol(argv[2], NULL, 10));
            
        if (error != 0) {
            return 2;
        } else {
            return 0;
        }
    }

}

