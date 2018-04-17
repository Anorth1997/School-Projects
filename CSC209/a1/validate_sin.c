#include <stdio.h>
#include <stdlib.h>

int populate_array(int sin, int *sin_array);
int check_sin(int *sin_array);


int main(int argc, char **argv) {
    // TODO: Verify that command line arguments are valid.
    if (!(argc == 2)) {
	    return 1;
    }
    
    int sin_number;
    int *sin_array = malloc(sizeof(int) * 9);
    // TODO: Parse arguments and then call the two helpers in sin_helpers.c
    // first_step, transfer the sin input to an integer.
    sin_number = strtol(argv[1], NULL, 10);
    
    // to verify the SIN given as a command line argument.
    if (populate_array(sin_number, sin_array) == 1) {
    	printf("Invalid SIN\n");
        
    } else {
    	if (check_sin(sin_array) == 1) {
	        printf("Invalid SIN\n");
            
	    } else {
	    printf("Valid SIN\n");
	    }
    }
    free(sin_array);
  
    return 0;
}
