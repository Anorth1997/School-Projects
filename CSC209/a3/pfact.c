#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

#include "filter.h"


/* A helper function that takes value of factor1,
 * factor2 and n to print the conclusion that if n is a prime or 
 * product of two primes or not product of two primes.
 */

void if_prime(int n, int factor1, int factor2) {

    if (factor1 == 0 && factor2 == 0) {
        printf("%d is prime\n", n);
    } else if (factor2 == 0) {
        if ((factor1 * factor1) == n) {
            printf("%d %d %d\n", n, factor1, factor1);
        } 
        else if (factor1 == n){
            printf("%d is prime\n", n);
        }
        else {
            printf("%d is not the product of two primes\n", n);
        }
    } 
    else {
        if (factor1 * factor1 == n) {
            printf("%d %d %d\n", n, factor1, factor1);
        }
        else if (factor1 * factor2 == n) {
            printf("%d %d %d\n", n, factor1, factor2);
        } else {
            printf("%d is not the product of two primes\n", n);
        }
    }
}

/* A helper function to check if the second argument is a valid argument
 * that is, it is a positive integer. This function returns -1 if it is not 
 * a positive integer, anything else represents the integer representation of second argument.
 */
int if_positive_integer(char *argv) {
  
    for (int i = 0; argv[i] != '\0'; i++) { // make sure it's digit only
        if (isdigit(argv[i]) == 0) {
            fprintf(stderr, "Usage:\n\tpfact n\n");
            return -1;
        }
    }
    
    return strtol(argv, NULL, 10);
}



int main(int argc, char **argv) {
    
    if (argc != 2) {
        fprintf(stderr, "Usage:\n\tpfact n\n");
        exit(1);
    }  

    /*
     * Check if the second argument is a positive integer
     */
    
    int n = if_positive_integer(argv[1]);
    if (n == -1 || n == 0) {
        fprintf(stderr, "Usage:\n\tpfact n\n");
        exit(1);
    }


    // declare variable name for two pipes that I will use later
    int fd[2][2];

    /* this is an identical flag to decide that if the future child process will 
     * use fd[0] or fd[1] as reading end or writing end.
     * if idp = 0, that means the child process calls filter by using fd[0] as reading pipe
     * and using fd[1] as writing end, vice versa.
     *
     */  
    int idp = 0;
    

    if (pipe(fd[idp]) == -1) {
        perror("pipe\n");
        exit(1);
    }

    int master_or_filter = fork();

    if (master_or_filter < 0) {
        perror("fork\n");
        exit(1);
    } else if (master_or_filter == 0) { //  filter branch processes
        
        
        if (close(fd[idp][1]) == -1) {
            perror("close writing end of pipe fd[idp]\n");
            exit(1);
        }
        
        int factor1 = 0;
        int factor2 = 0;

        // by this step, the initial input in the very first created pipe [2 ... N] -> [3 ... N] 
        int m;
        int flag;
        if ((flag = read(fd[idp][0], &m, sizeof(int))) == -1) {  // not sure
            perror("read m\n");
            exit(2);
        } else if (flag == 0) {
            if_prime(n, factor1, factor2);
            exit(0);
        }

        // check if the first filter value m = 2 is a factor of n
        if (n % m == 0) {
            if (factor1 == 0) {
                factor1 = m;
            } else {
                factor2 = m;
            }
        }
        
        
        while(m < sqrt(n) && (factor2 == 0)){

            // pipe a filter_fd, the data that written into this pipe will be read by next filter child
            if (pipe(fd[!idp]) == -1) {
                perror("pipe\n");
                exit(2);
            }

            int pid;
            pid = fork();
            
            if (pid < 0) {
                perror("fork in child\n");
                exit(2);
            } else if (pid > 0) { // filter parent
                if (close(fd[!idp][0]) == -1) {
                    perror("close reading end of pipe fd[!idp]\n");
                    exit(2);
                }

                // filter the values to next child.
                if (filter(m, fd[idp][0], fd[!idp][1]) != 0) {
                    perror("filter\n");
                    exit(2);
                }

                if (close(fd[idp][0]) == -1) {
                    perror("close reading end of pipe fd[idp]\n");
                    exit(2);
                }

                if (close(fd[!idp][1]) == -1) {
                    perror("close reading end of pipe fd[!idp]\n");
                    exit(2);
                }
                

                int status;
                int filter_num;
                if (wait(&status) == -1) {
                    perror("wait\n");
	                exit(1);
                }
                if (WIFEXITED(status)) {
                    filter_num = WEXITSTATUS(status) + 1;
                    exit(filter_num);
                }

            } else { // filter child
                
                idp = !idp;

                if (pipe(fd[!idp]) == -1) {
                    perror("pipe fd[!idp]\n");
                    exit(2);
                }

                if (close(fd[!idp][0]) == -1) {
                    perror("closing reading end of pipe fd[!idp]\n");
                    exit(2);
                }

                if (close(fd[idp][1]) == -1) {
                    perror("closing writing end of pipe fd[idp]\n");
                    exit(2);
                }
                
                // read filter value m from filter_fd
                if (read(fd[idp][0], &m, sizeof(int)) != sizeof(int)) {
                    perror("reading m in child process\n");
                    exit(2);
                }

                // check if m is a factor
                if (n % m == 0) {
                    if (factor1 == 0 && factor2 == 0) {
                        factor1 = m;
                    } else if (factor2 == 0) {
                        factor2 = m;
                    }
                }



            }    
        }

        int garbage;
        int error;
        
        
        // only the very bottom child process gets here
        if (factor1 != 0 && factor2 == 0) { // special case, only 1 factor found
            int temp;
            while((read(fd[idp][0], &temp, sizeof(int)) == sizeof(int)) && factor2 == 0) {
                if (n % temp == 0) {
                    factor2 = temp;
                }
            }
        } else if (factor1 == 0 && factor2 == 0) {   
            int temp;
            while(read(fd[idp][0], &temp, sizeof(int)) == sizeof(int)) {
                if (n % temp == 0) {
                    factor1 = temp;
                }
            }
        }
        
        if_prime(n, factor1, factor2);

        while ((error = read(fd[idp][0], &garbage, sizeof(int))) == sizeof(int)){
            // this while loop just empty the left over not needed integers, no body needed here
        }

        if (close(fd[idp][0]) == -1) {
            perror("close reading end of pipe fd[idp] before exit\n");
            exit(1);
        }

        exit(0);

    } else {  // master process
        if (close(fd[idp][0] == -1)) {
            perror("close reading end of pipe fd[idp] in master process\n");
            exit(1);
        }
            
        for (int i = 2; i <= n; i++){
            if(write(fd[idp][1], &i, sizeof(int)) == -1){
                perror("writing child initial inputs to pipe fd[idp]\n");
                close(fd[0][1]);
                exit(1);
            }
        }

        if (close(fd[idp][1]) == -1) {
            perror("close writing end of pipe fd[idp] in master process\n");
            exit(1);
        }

    }

    // Only the master gets here

    int result;
    int status;
    if (wait(&status) == -1) {
        perror("wait");
        exit(1);
    }
    if (WIFEXITED(status)) {
        result = WEXITSTATUS(status);
    }

    printf("Number of filters = %d\n", result);
    
    return 0;
}


