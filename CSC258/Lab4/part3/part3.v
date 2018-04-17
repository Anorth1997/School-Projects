module part3(SW, KEY, LEDR);
	input [9:0] SW;
	input [3:0] KEY;
	output [9:0] LEDR;
	
	shifter init(
		.LoadVal(SW[7:0]),
		.Load_n(KEY[1]),
		.ShiftRight(KEY[2]),
		.ASR(KEY[3]),
		.clk(KEY[0]),
		.reset_n(SW[9]),
		.Q(LEDR[7:0])
		);
		
endmodule


module shifter(LoadVal, Load_n, ShiftRight, ASR, clk, reset_n, Q);
	input [7:0] LoadVal;
	input Load_n, ShiftRight, ASR, clk, reset_n;
	output [7:0] Q;
	
	wire asr_out; // store the output of mux2to1 asr, 0 leads Q[7] = 0, 1 leads Q[7] = Q[7];
	wire [7:0] shifterbit_out; // store the output of each shifterbit
	
	
	mux2to1 asr(
		.x(0),
		.y(shifterbit_out[7]),
		.s(ASR),
		.m(asr_out)
		);
		
	
	shifterbit s7(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(asr_out),
		.load_val(LoadVal[7]),
		.out(shifterbit_out[7])
		);
		
	shifterbit s6(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[7]),
		.load_val(LoadVal[6]),
		.out(shifterbit_out[6])
		);
	
	shifterbit s5(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[6]),
		.load_val(LoadVal[5]),
		.out(shifterbit_out[5])
		);

	shifterbit s4(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[5]),
		.load_val(LoadVal[4]),
		.out(shifterbit_out[4])
		);

	shifterbit s3(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[4]),
		.load_val(LoadVal[3]),
		.out(shifterbit_out[3])
		);
		
	shifterbit s2(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[3]),
		.load_val(LoadVal[2]),
		.out(shifterbit_out[2])
		);
		
	shifterbit s1(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[2]),
		.load_val(LoadVal[1]),
		.out(shifterbit_out[1])
		);
		
	shifterbit s0(
		.shift(ShiftRight),
		.load_n(Load_n),
		.clk(clk),
		.reset_n(reset_n),
		.in(shifterbit_out[1]),
		.load_val(LoadVal[0]),
		.out(shifterbit_out[0])
		);
		
	assign Q[7:0] = shifterbit_out[7:0];
		
endmodule

		
module shifterbit(shift, load_n, clk, reset_n, in, load_val, out);
	input shift, load_n, clk, reset_n, in, load_val;
	output out;
	
	wire connection1; // store the output of first mux2to1
	wire connection2; // store the output of second mux2to1
	wire connection3;	// store the output of register
	
	mux2to1 m1(
		.x(connection3),
		.y(in),
		.s(shift),
		.m(connection1)
		);
	
	mux2to1 m2(
		.x(load_val),
		.y(connection1),
		.s(load_n),
		.m(connection2)
		);
		
	register r(
		.d(connection2),
		.clk(clk),
		.reset_n(reset_n),
		.q(connection3)
		);
	
		
	assign out = connection3;
	
endmodule
	
module mux2to1(x, y, s, m);
    input x; //selected when s is 0
    input y; //selected when s is 1
    input s; //select signal
    output m; //output
  
    assign m = s & y | ~s & x;
    // OR
    // assign m = s ? y : x;

endmodule

module register(d, clk, reset_n, q);
	input d;
	input clk, reset_n;
	output q;
	reg q; 

	always @(posedge clk) 
	begin 
		if (reset_n == 1'b0) 
			
			q <= 1'b0;
		
		else 
			q <= d;
	end 
endmodule