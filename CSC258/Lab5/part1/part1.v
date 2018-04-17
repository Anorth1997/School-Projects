module part1(SW, KEY, HEX0, HEX1);
	input [9:0] SW;
	input [3:0] KEY;
	output [6:0] HEX0;
	output [6:0] HEX1;


	wire [7:0] out;
	
	eightbitcounter e0(
		.enable(SW[1]),
		.clk(KEY[0]),
		.clear_b(SW[0]),
		.Q(out)
		);

	SevenSegmentDecoder s0(
		.c(out[3:0]),
		.ss_out(HEX0)
		);

	SevenSegmentDecoder s1(
		.c(out[7:4]),
		.ss_out(HEX1)
		);
endmodule
	


module SevenSegmentDecoder(c,ss_out);
	input [3:0] c; //the bcd input
	output [6:0] ss_out; //the seven segements
	
	assign ss_out[0] = ~c[3] & ~c[2] & ~c[1] & c[0] | ~c[3] & c[2] & ~c[1] & ~c[0] | c[3] & ~c[2] & c[1] & c[0] | c[3] & c[2] & ~c[1] & c[0];
	assign ss_out[1] = c[3] & c[1] & c[0] | c[2] & c[1] & ~c[0] | ~c[3] & c[2] & ~c[1] & c[0] | c[3] & c[2] & ~c[0];
	assign ss_out[2] = ~c[3] & ~c[2] & c[1] & ~c[0] | c[3] & c[2] & ~c[0] | c[3] & c[2] & c[1];
	assign ss_out[3] = ~c[3] & ~c[2] & ~c[1]& c[0] | ~c[3] & c[2] & ~c[1] & ~c[0] | c[2] & c[1] & c[0] | c[3] & ~c[2] & c[1] & ~c[0];
	assign ss_out[4] = ~c[3] & c[0] | ~c[3] & c[2] & ~c[1] | ~c[2] & ~c[1] & c[0];
	assign ss_out[5] = ~c[3] & ~c[2] & c[0] | ~c[3] & ~c[2] & c[1] | ~c[3] & c[1] & c[0] | c[3] & c[2] & ~c[1] & c[0];
	assign ss_out[6] = ~c[3] & ~c[2] & ~c[1] | ~c[3] & c[2] & c[1] & c[0] | c[3] & c[2] & ~c[1] & ~c[0];
	
endmodule	

module eightbitcounter(enable, clk, clear_b, Q);
	input enable, clk, clear_b;
	output [7:0] Q;
	
	wire [6:0] connection;
	
	tflipflop t0(
		.enable(enable),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[0])
		);
	
	assign connection[0] = Q[0] && enable;
	
	tflipflop t1(
		.enable(connection[0]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[1])
		);
	
	assign connection[1] = Q[1] && connection[0];
	
	tflipflop t2(
		.enable(connection[1]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[2])
		);
	
	assign connection[2] = Q[2] && connection[1];
	
	tflipflop t3(
		.enable(connection[2]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[3])
		);
		
	assign connection[3] = Q[3] && connection[2];
		
	tflipflop t4(
		.enable(connection[3]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[4])
		);
		
	assign connection[4] = Q[4] && connection[3];	
		
	tflipflop t5(
		.enable(connection[4]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[5])
		);
		
	assign connection[5] = Q[5] && connection[4];	
		
	tflipflop t6(
		.enable(connection[5]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[6])
		);
		
	assign connection[6] = Q[6] && connection[5];
	
	tflipflop t7(
		.enable(connection[6]),
		.clk(clk),
		.clear_b(clear_b),
		.Q(Q[7])
		);

endmodule		
	
	

module tflipflop(enable, clk, clear_b, Q);
	input enable, clk, clear_b;
	output Q;
	reg Q;
	
	always @(posedge clk, negedge clear_b)
	begin
		if (clear_b == 1'b0) 

			Q <= 0;

		else 
			Q <= enable ^ Q;
	end
endmodule
	