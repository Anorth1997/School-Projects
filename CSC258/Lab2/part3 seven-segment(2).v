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
	