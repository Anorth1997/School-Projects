module part2(SW, CLOCK_50, HEX0);
	input [2:0] SW;
	input CLOCK_50;
	output [6:0] HEX0;
	
	wire [3:0] connection;
	
	whole w1(
		.clk(CLOCK_50),
		.reset_r(SW[2]),
		.reset_d(SW[2]),
		.s(SW[1:0]),
		.out(connection)
		);
		
	SevenSegmentDecoder s0(
		.c(connection),
		.ss_out(HEX0)
		);
		
endmodule

module whole(clk, reset_r, reset_d, s, out);
	input [1:0] s; //selecters
	input clk;
	input reset_r; //reset for ratedivider
	input reset_d; //reset for displaycounter
	output [3:0] out;
	
	reg [27:0] max;
	wire connection1;
	
	
	always @(*)
	begin
		case(s[1:0])
			2'b00: max = 0;
			2'b01: max = 28'b0010111110101111000001111111; // 1s, 1Hz
			2'b10: max = 28'b0101111101011110000011111111; // 2s, 0.5Hz
			2'b11: max = 28'b1011111010111100000111111111; // 4s, 0.25Hz
		endcase
	end

	RateDivider r1(
		.max(max),
		.clock(clk),
		.reset_n(reset_r),
		.enable(connection1)
		);
	
	DisplayCounter d1(
		.enable(connection1),
		.clk(clk),
		.reset(reset_d),
		.Q(out)
		);
		
endmodule 

module DisplayCounter(enable, clk, reset, Q);
	input enable, clk;
	input reset;
	output [3:0] Q;
	
	reg [3:0] Q;
	
	
	always @(posedge clk) 
	begin 
		if (reset == 1'b0) 
			Q <= 0;
		else if (enable == 1'b1)
			Q <= Q + 1'b1;
	end 
endmodule 



module RateDivider(max, clock, reset_n, enable);
	input [27:0] max;
	input clock, reset_n;
	output enable;
	
	reg [27:0] q;
	
	always @(posedge clock) 
	begin 
		if ((reset_n) == 1'b0)
			q <= 0;
		else 
			if (q == 0) 
				q <= max;
			else 
				q <= q - 1'b1;
		
	end
	
	assign enable = (q == 0) ? 1 : 0;
	
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