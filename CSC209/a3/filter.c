#include <unistd.h>
#include <stdio.h>

#include "filter.h"


/* A helper function to generate the filter.
 *
 * It returns 0 if completes without encountering error or returns 1 if counters error.
 */
int filter(int n, int read_fd, int write_fd) {
    int possible_prime;
    int error;
    while ((error = read(read_fd, &possible_prime, sizeof(int))) == sizeof(int)){
        if (possible_prime % n != 0) {
            if (write(write_fd, &possible_prime, sizeof(int)) != sizeof(int)) {
                perror("fail writing in filter\n");
                return 1;
            }
        }
    }

    if (error == -1) {
        perror("filter.c\n");
        return 1;
    }
    return 0;
}

    // int filter(int m, int read_fd, int write_fd) {
    //     int len;
    //     if (read(read_fd, &len, sizeof(int)) == -1) {
    //         perror("filter, failed read in len");
    //         return 1;
    //     }

    //     int data_in[len];
    //     if (read(read_fd, data_in, sizeof(int) * len) != sizeof(int) * len) {
    //         perror("filter, failed to read data_in array");
    //         return 1;
    //     }

    //     int result_len = 0;
    //     for (int i_1 = 0; i_1 < len; i_1++) {
    //         if (data_in[i_1] % m != 0) {
    //             result_len++;
    //         }
    //     }

    //     int data_out[result_len];
    //     int u = 0;
    //     int i_2 = 0;
    //     while(i_2 < len) {
    //         if (data_in[i_2] % m != 0) {
    //             data_out[u] = data_in[i_2];
    //             u++;
    //         }
    //         i_2++;
    //     }

        
    //     if (write(write_fd, &result_len, sizeof(int)) != sizeof(int)){
    //         perror("filter, failed write in result_len");
    //         return 1;
    //     }

    //     if (write(write_fd, data_out, sizeof(int) * result_len) != sizeof(int) * result_len) {
    //         perror("filter, failed write in data_out");
    //         return 1;
    //     }
    // }