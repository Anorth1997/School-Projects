// TODO: Implement populate_array
/*
 * Convert a 9 digit int to a 9 element int array.
 */
int populate_array(int sin, int *sin_array) {
    int i;
    for (i = 9; i > 0; i--) {
    	sin_array[i-1] = sin % 10;
	    sin = sin / 10;
    }
    
    if (sin != 0 || sin_array[0] == 0) {
        return 1;
    }

    return 0;
}

// TODO: Implement check_sin
/* 
 * Return 0 (true) iff the given sin_array is a valid SIN.
 */
int check_sin(int *sin_array) {
    
    int check[9] = {1,2,1,2,1,2,1,2,1};
    int sum = 0;
    int i, u; //the loop indicators.
    int first_time[9];
    
    //first step to multiple the SIN number with special nine digits.
    for (i = 0; i < 9; i++) {
    
    	int mult = check[i] * sin_array[i];
	
	if (mult >= 10) {
	    first_time[i] = (mult % 10) + (mult / 10);
	} else {
	    first_time[i] = mult;
	}
    }
    
    // second step to sum the digits of the result from step one.
    for (u = 0; u < 9; u++) {
    	sum += first_time[u];
    }
    
    // validate step, determined by whether divisible by 10 or not.
    if (sum % 10 == 0) {
    	return 0;
    }
	
    return 1;
}
