module part3
	(
		CLOCK_50,						//	On Board 50 MHz
		// Your inputs and outputs here
      SW,
		KEY,
		// The ports below are for the VGA output.  Do not change.
		VGA_CLK,   						//	VGA Clock
		VGA_HS,							//	VGA H_SYNC
		VGA_VS,							//	VGA V_SYNC
		VGA_BLANK_N,						//	VGA BLANK
		VGA_SYNC_N,						//	VGA SYNC
		VGA_R,   						//	VGA Red[9:0]
		VGA_G,	 						//	VGA Green[9:0]
		VGA_B   						//	VGA Blue[9:0]
	);

	input			CLOCK_50;				//	50 MHz
	input   [2:0]   SW;
	input   [0:0]   KEY;

	// Declare your inputs and outputs here
	// Do not change the following outputs
	output			VGA_CLK;   				//	VGA Clock
	output			VGA_HS;					//	VGA H_SYNC
	output			VGA_VS;					//	VGA V_SYNC
	output			VGA_BLANK_N;				//	VGA BLANK
	output			VGA_SYNC_N;				//	VGA SYNC
	output	[9:0]	VGA_R;   				//	VGA Red[9:0]
	output	[9:0]	VGA_G;	 				//	VGA Green[9:0]
	output	[9:0]	VGA_B;   				//	VGA Blue[9:0]
	
	wire resetn;
	assign resetn = KEY[0];
	
	// Create the colour, x, y and writeEn wires that are inputs to the controller.
	wire [2:0] colour;
	wire [7:0] x;
	wire [6:0] y;
	wire writeEn;

	// Create an Instance of a VGA controller - there can be only one!
	// Define the number of colours as well as the initial background
	// image file (.MIF) for the controller.
	vga_adapter VGA(
			.resetn(resetn),
			.clock(CLOCK_50),
			.colour(colour),
			.x(x),
			.y(y),
			.plot(writeEn),
			/* Signals for the DAC to drive the monitor. */
			.VGA_R(VGA_R),
			.VGA_G(VGA_G),
			.VGA_B(VGA_B),
			.VGA_HS(VGA_HS),
			.VGA_VS(VGA_VS),
			.VGA_BLANK(VGA_BLANK_N),
			.VGA_SYNC(VGA_SYNC_N),
			.VGA_CLK(VGA_CLK));
		defparam VGA.RESOLUTION = "160x120";
		defparam VGA.MONOCHROME = "FALSE";
		defparam VGA.BITS_PER_COLOUR_CHANNEL = 1;
		defparam VGA.BACKGROUND_IMAGE = "black.mif";
			
	combination u0(
						.colour_in(SW[2:0]),
						.clock(CLOCK_50),
						.resetn(resetn),
						.x_out(x),
						.y_out(y),
						.colour_out(colour),
						.plot(writeEn)
						);
    
endmodule

module combination(colour_in, clock, resetn, x_out, y_out, colour_out, plot);
	input [2:0]colour_in;
	input clock, resetn;
	output [7:0]x_out;
	output [6:0]y_out;
	output [2:0]colour_out;
	output plot;
	wire ld_x, ld_y, display, erase;
	wire [7:0]x_in;
	wire [6:0]y_in;
	wire [4:0]count;
	
	datapath d0(
					.x_in(x_in),
					.y_in(y_in),
					.colour_in(colour_in),
					.alu_op(count[3:0]),
					.clock(clock),
					.resetn(resetn),
					.ld_x(ld_x),
					.ld_y(ld_y),
					.display(display),
					.erase(erase),
					.x_out(x_out),
					.y_out(y_out),
					.colour_out(colour_out)
					);

	control c0(
				  .clock(clock), 
				  .resetn(resetn), 
				  .x_count(x_in),
				  .y_count(y_in),
				  .count(count),
				  .ld_x(ld_x), 
				  .ld_y(ld_y), 
				  .display(display), 
				  .erase(erase),
				  .plot(plot)
				  );
				  
endmodule

module datapath(x_in, y_in, colour_in, alu_op, clock, resetn, ld_x, ld_y, display, erase, x_out, y_out, colour_out);
	input [7:0]x_in;
	input [6:0]y_in;
	input [2:0]colour_in;
	input [3:0]alu_op;
	input clock, resetn, ld_x, ld_y, display, erase;
	output reg [7:0]x_out;
	output reg [6:0]y_out;
	output reg [2:0]colour_out;
	reg [7:0]x;
	reg [6:0]y;
	
	always@(posedge clock)
		begin: load
			if(!resetn)
				begin 
					x <= 8'b00000000;
					y <= 7'b0000000;
				end
			
			else
				begin
					if(ld_x) 
						x <= x_in;
					if(ld_y) 
						y <= y_in;
					if(display)
						begin
							x_out <= x + alu_op[1:0];
							y_out <= y + alu_op[3:2];
							colour_out <= colour_in;
						end
					if(erase)
						begin
							x_out <= x + alu_op[1:0];
							y_out <= y + alu_op[3:2];
							colour_out <= 3'b000;
						end
				end
		end
		
endmodule

module control(clock, resetn, x_count, y_count, count, ld_x, ld_y, display, erase, plot);
	input resetn, clock;
	reg [19:0]time_count;
	reg [3:0]frame_count; 
	reg [1:0]xy_dir;
	output reg [7:0]x_count;
	output reg [6:0]y_count;
	output reg ld_x, ld_y, display, erase, plot;
   output reg [4:0]count;

	reg [2:0]current_state, next_state;
	
	localparam  S_START = 3'd0,
					S_DRAW= 3'd1,
					S_DELAY = 3'd2,
					S_ERASE = 3'd3,
					S_UPDATE = 3'd4;
	
	always @(*)
		begin: states
			case (current_state)
				S_START: next_state = S_DRAW;
				S_DRAW: next_state = (count == 5'b10000) ? S_DELAY : S_DRAW;
				S_DELAY: next_state = (frame_count == 4'd00) ? S_ERASE : S_DELAY;
				S_ERASE: next_state = (count == 5'b10000) ? S_UPDATE : S_ERASE;
				S_UPDATE: next_state = S_DRAW;
				default: next_state = S_START;
			endcase
		end
					
	always @(*)
		begin: signals
			ld_x = 1'b0;
			ld_y = 1'b0;
			erase = 1'b0;
			display = 1'b0;
			plot = 1'b0;
		
			case (current_state)
				S_START: begin
					x_count = 8'd0;
					y_count = 7'd60;
					xy_dir = 2'b10;
					time_count = 19'd833333;
					frame_count = 4'd15;
					count = 4'b0000;
					end
					
				S_DRAW: begin
					ld_x = 1'b1;
					ld_y = 1'b1;
					display = 1'b1;
					plot = 1'b1;
					end
					
				S_ERASE: begin
					ld_x = 1'b1;
					ld_y = 1'b1;
					erase = 1'b1;
					plot = 1'b1;
					end
					
				S_UPDATE: begin
					case(xy_dir)
						2'b00: begin
							if (x_count - 1'd1 < 8'd0)
								begin
								xy_dir[1] = 1'b1;
								x_count = x_count + 1'd1;
								end
							if (y_count - 1'd1 < 7'd0)
								begin
								xy_dir[0] = 1'b1;
								y_count = y_count + 1'd1;
								end
							else 
								x_count = x_count - 1'd1;
								y_count = y_count - 1'd1;
							end
							
						2'b01: begin
							if (x_count - 1'd1 < 8'd0)
								begin
								xy_dir[1] = 1'b1;
								x_count = x_count + 1'd1;
								end
							if (y_count + 1'd1 < 7'd120)
								begin
								xy_dir[0] = 1'b0;
								y_count = y_count - 1'd1;
								end
							else 
								x_count = x_count - 1'd1;
								y_count = y_count + 1'd1;
							end
							
						2'b10: begin
							if (x_count + 1'd1 > 8'd160)
								begin
								xy_dir[1] = 1'b0;
								x_count = x_count - 1'd1;
								end
							if (y_count - 1'd1 < 7'd0)
								begin
								xy_dir[0] = 1'b1;
								y_count = y_count + 1'd1;
								end
							else 
								x_count = x_count + 1'd1;
								y_count = y_count - 1'd1;
							end
							
						2'b11: begin
							if (x_count + 1'd1 > 8'd160)
								begin
								xy_dir[1] = 1'b0;
								x_count = x_count - 1'd1;
								end
							if (y_count + 1'd1 > 7'd120)
								begin
								xy_dir[0] = 1'b0;
								y_count = y_count - 1'd1;
								end
							else 
								x_count = x_count + 1'd1;
								y_count = y_count + 1'd1;
							end
						
					endcase
				end
	
			endcase
		end

	always@(posedge clock)
		begin
			if(!resetn)
				count <= 5'b00000;
			else if((current_state == S_DRAW)||(current_state == S_ERASE))
				begin
					if(count == 5'b10000)
						count <= 5'b00000;
						
					else
						count <= count + 1'b1;
				end
		end
	
	always @(posedge clock)
		begin
			if(!resetn)
				time_count <= 19'd833333;
			else if(current_state == S_DELAY)
				begin
					if (time_count == 19'd0)
						time_count <= 19'd833333;
					else 
						time_count <= time_count - 1'd1;
				end
		end
	
	always @(posedge clock)
		begin
			if(!resetn)
				frame_count <= 4'd15;
			else if(current_state == S_DELAY)
				begin
					if (frame_count == 4'd0)
						frame_count <= 4'd15;
					else if(time_count == 19'd0)
						frame_count <= frame_count - 1'd1;
				end
		end
	
	always @(posedge clock)
		begin 
        if(!resetn)
            current_state <= S_START;
        else
            current_state <= next_state;
		end 
endmodule				