module ripplecarryadder(A, B, cin, S, cout);
	input [3:0] A;
	input [3:0] B;
	input cin;
	output [3:0] S;
	output cout;
	
	wire Connection1, Connection2, Connection3;
	
	fulladder f1(A[0], B[0], cin, Connection1, S[0]);
	fulladder f2(A[1], B[1], Connection1, Connection2, S[1]);
	fulladder f3(A[2], B[2], Connection2, Connection3, S[2]);
	fulladder f4(A[3], B[3], Connection3, cout, S[3]);
	
endmodule
	
	
	




module fulladder(a, b, carryin, carryout, sum);
	input a, b, carryin; // adding a and b with carryin from the previous bit's carryout
	output carryout, sum; // carryout for the next bit's carryin, and sum for XOR of a and b
	
	assign carryout = (a && b) | (b && carryin) | (a && carryin);
	assign sum = a ^ b ^ carryin;
	
endmodule


	
	