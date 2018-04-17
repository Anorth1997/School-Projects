module part2(SW, KEY, HEX0, HEX4, HEX5, LEDR);
	input [9:0] SW;
	input [3:0] KEY;
	output [6:0] HEX0;
	output [6:0] HEX4;
	output [6:0] HEX5;
	output [9:0] LEDR;
	
	wire [7:0] ALUout;
	wire [7:0] register_out;

	
	
	register reg1(
		.d(ALUout[7:0]),
		.clk(KEY[0]),
		.reset_n(SW[9]),
		.q(register_out[7:0])
		);
	
	alu a1(
		.A(SW[3:0]),
		.B(register_out[3:0]),
		.func(SW[7:5]),
		.ALUout(ALUout[7:0])
		);
	
	SevenSegmentDecoder h0(
		.c3(SW[3]),
		.c2(SW[2]),
		.c1(SW[1]),
		.c0(SW[0]),
		.ss_out(HEX0[6:0])
		);
	
	SevenSegmentDecoder h4(
		.c3(register_out[3]),
		.c2(register_out[2]),
		.c1(register_out[1]),
		.c0(register_out[0]),
		.ss_out(HEX4[6:0])
		);
	
	SevenSegmentDecoder h5(
		.c3(register_out[7]),
		.c2(register_out[6]),
		.c1(register_out[5]),
		.c0(register_out[4]),
		.ss_out(HEX5[6:0])
		);
	
	assign LEDR[7:0] = register_out[7:0];
		
endmodule
	
module register(d, clk, reset_n, q);
	input [7:0] d;
	input clk, reset_n;
	output [7:0] q;
	reg [7:0] q; /*synthesis keep */

	always @(posedge clk) 
	begin 
		if (reset_n == 1'b0) 
			
			q <= 8'b00000000;
		
		else 
			q <= d;
	end 
endmodule

module alu(A,B,func,ALUout);
	input [3:0] A;
	input [3:0] B;
	input [2:0] func;
	output [7:0] ALUout;
	reg [7:0] ALUout;
	
	wire [3:0] f0s; // output storage for f0 sum
	wire f0cout; // output storage for f0 carry out
	wire [3:0] f1s; //output storage for f1 sum
	wire f1cout; // output storage for f1 carry out
	
	ripplecarryadder f0(A[3:0], 4'b0001, 1'b0, f0s, f0cout);  //setup for function0
	ripplecarryadder f1(A[3:0], B[3:0], 1'b0, f1s, f1cout);  //setup for function1
	
	always @(*) 
	begin
		case (func[2:0]) 
			3'b000: ALUout[7:0] = {3'b000,f0cout,f0s};
			3'b001: ALUout[7:0] = {3'b000, f1cout, f1s};
			3'b010: ALUout[7:0] = A+B;
			3'b011: ALUout[7:0] = {A|B, A^B};
			3'b100: ALUout[7:0] = {7'b0000_000, A[3]|A[2]|A[1]|A[0]|B[3]|B[2]|B[1]|B[0]};
			3'b101: ALUout[7:0] = B << A;
			3'b110: ALUout[7:0] = B >> A;
			3'b111: ALUout[7:0] = A*B;
		endcase
	end
endmodule
	

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


module SevenSegmentDecoder(c3,c2,c1,c0,ss_out);
	input c3,c2,c1,c0; //the bcd input
	output [6:0] ss_out; //the seven segements
	
	assign ss_out[0] = ~c3 & ~c2 & ~c1 & c0 | ~c3 & c2 & ~c1 & ~c0 | c3 & ~c2 & c1 & c0 | c3 & c2 & ~c1 & c0;
	assign ss_out[1] = c3 & c1 & c0 | c2 & c1 & ~c0 | ~c3 & c2 & ~c1 & c0 | c3 & c2 & ~c0;
	assign ss_out[2] = ~c3 & ~c2 & c1 & ~c0 | c3 & c2 & ~c0 | c3 & c2 & c1;
	assign ss_out[3] = ~c3 & ~c2 & ~c1 & c0 | ~c3 & c2 & ~c1 & ~c0 | c2 & c1 & c0 | c3 & ~c2 & c1 & ~c0;
	assign ss_out[4] = ~c3 & c0 | ~c3 & c2 & ~c1 | ~c2 & ~c1 & c0;
	assign ss_out[5] = ~c3 & ~c2 & c0 | ~c3 & ~c2 & c1 | ~c3 & c1 & c0 | c3 & c2 & ~c1 & c0;
	assign ss_out[6] = ~c3 & ~c2 & ~c1 | ~c3 & c2 & c1 & c0 | c3 & c2 & ~c1 & ~c0;
	
endmodule

