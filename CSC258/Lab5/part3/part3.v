module part3(CLOCK_50, SW, KEY, LEDR);
	input CLOCK_50;
	input [1:0] KEY;
	input [2:0] SW;
	output [9:0] LEDR;
	
	morsecode m1(
		.clock_50(CLOCK_50),
		.selecters(SW), 
		.display(KEY[1]), 
		.reset(KEY[0]), 
		.out_light(LEDR[0])
		);
		
endmodule


module morsecode(clock_50, selecters, display, reset, out_light);
	input [2:0] selecters;
	input display, reset, clock_50;
	output out_light;
	
	wire [13:0] LUT_to_Shift;
	wire signal;
	
	LUT L1(
		.s(selecters),
		.q(LUT_to_Shift)
		);
	
	ShiftRegister s1(
		.display(display),
		.bit(LUT_to_Shift),
		.clock(signal),
		.reset(reset),
		.output_seq(out_light)
		);

	RateDivider r1(
		.clock(clock_50),
		.reset_n(reset),
		.out(signal)
		);
		
	
endmodule
	

module RateDivider(clock, reset_n, out);
	input clock, reset_n;
	output out;
	
	reg [21:0] q;
	
	always @(posedge clock) 
	begin 
		if ((reset_n) == 1'b0)
			q <= 0;
		else 
			if (q == 0) 
				q <= 22'b1001100010010110100000;
			else 
				q <= q - 1'b1;
		
	end
	
	assign out = (q == 0) ? 1 : 0;
	
endmodule 

module LUT(s, q);
	input [2:0] s; //selecters
	output [13:0] q; // 14-bit representation of letters
	reg [13:0] q;
	
	always @(*) 
	begin 
		case(s[2:0])
			3'b000: q = 14'b10101000000000;
			3'b001: q = 14'b11100000000000;
			3'b010: q = 14'b10101110000000;
			3'b011: q = 14'b10101011100000;
			3'b100: q = 14'b10111011100000;
			3'b101: q = 14'b11101010111000;
			3'b110: q = 14'b11101011101110;
			3'b111: q = 14'b11101110101000;
		endcase
	end
	
endmodule


module ShiftRegister(display, bit, clock, reset, output_seq);
	input display;
	input [13:0] bit;
	input clock;
	input reset;
	output output_seq;
	reg [13:0] q;
	
	wire counter = 14;
	
	always @(posedge clock, negedge reset, negedge display)
	begin 
		if (reset == 0)
			q = 14'b00000000000000;
		else 
			if (display == 0)
				q <= bit;
			else 
				q = q << 1'b1;
	end
	
	assign output_seq = q[13];

endmodule
	
	