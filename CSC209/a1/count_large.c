#include <stdio.h>
#include <stdlib.h>


// TODO: Implement a helper named check_permissions that matches the prototype below.
int check_permissions(char *file_per, char *required_per) {
    int i;
    
    for (i = 0; i < 9; i++) {
    	if ((required_per[i] != '-') && (file_per[i] != required_per[i])) {
            return 1;
	    } 
    }

    return 0;
}


int main(int argc, char** argv) {
    if (!(argc == 2 || argc == 3)) {
        fprintf(stderr, "USAGE: count_large size [permissions]\n");
        return 1;
    }
    
    char buffer;
    int satisfied = 0;
    // skip the first line.
    while (scanf("%c", &buffer) != EOF) {

        if (buffer == '\n') {
            break;
        }
        
    }
   
    //initialize necessary checkers for both cases.
    int pos = 1;
    char *file_size = malloc(sizeof(char) * 10);
    int i = 0;

    // position checker, 0 implies buffer at ' ', 1 implies buffer not at ' '
    int check = 1;

    //start checking
    // first possible, only one argument, check file size only then
    if (argc == 2) {
        while (scanf("%c", &buffer) != EOF) {
            // pos increment by one if check changes from 0 to 1, refresh back to 1 if encounters new line character.
            if (buffer == ' ') {
                check = 0;
            } else if (check == 0) {
                check = 1;
                pos++;
            } else if (buffer == '\n') {
                pos = 1;
            }  

            // compare or filling the file size and decide wheter increament satisfied by one.
            if (pos == 5 && check == 1) {
                file_size[i] = buffer;
                i++;
            } else if (pos == 5 && check == 0) {
                i = 0;
                if (strtol(file_size, NULL, 10) > strtol(argv[1], NULL, 10)) {
                        satisfied++;      
                }
		free(file_size);
                file_size = malloc(sizeof(char) * 10);
            }
        }
    } else { 
        char file_per[9];
        // u indicated the index at file_per array
        int u = 0;
        // permission checker, o implies true, 1 implies false
        int per_check;
        scanf("%c", &buffer); //skip the newline character, next line of code will skip the file type
        while (scanf("%c", &buffer) != EOF) {
            // pos increment by one if check changes from 0 to 1, refresh back to 1 if encounters new line character.
            if (buffer == ' ') {
                check = 0;
            } else if (check == 0) {
                check = 1;
                pos++;
            } else if (buffer == '\n') {
                scanf("%c", &buffer);
                scanf("%c", &buffer); //skip the new line character and filetype
                pos = 1;
            }  

            // compare or filling the file size and decide wheter increament satisfied by one.
            
            if (pos == 1 && check == 1) {
                file_per[u] = buffer;
                u++;
            } else if (pos == 1 && check == 0) {
                u = 0;
                per_check = check_permissions(file_per, argv[2]);
            } else if (pos == 5 && check == 1) {
                file_size[i] = buffer;
                i++;
            } else if (pos == 5 && check == 0) {
	    	
                i = 0;
                if (strtol(file_size, NULL, 10) > strtol(argv[1], NULL, 10) && per_check == 0) {
                        satisfied++;
                }
		free(file_size);
                file_size = malloc(sizeof(char) * 10);
            }  
        }
    }

    free(file_size);
    printf("%d\n", satisfied);    
    
    // TODO: Process command line arguments.
    

    // TODO Call check permissions as part of your solution to counting the files to
    // compute and print the correct value.

    return 0;
}
