// The size of our game board will be 40 x 80 pixes. Each block in our game is 4 x 4 pixels,
// thus the capacity of our game board is 10 x 20 blocks. The pixel coordinates of four corners
// of the game board is (60, 40), (60, 120), (100, 40), (100, 120) in respect of top-left, bottom-left,
// top-right and bottom-right.
module milestone3
	(
		CLOCK_50,						//	On Board 50 MHz
		// Your inputs and outputs here
        KEY,
        SW,
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
	input   [9:0]   SW;
	input   [3:0]   KEY;

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
	assign resetn =   KEY[0];
	assign start = ~KEY[1];
	
	// Create the colour, x, y and writeEn wires that are inputs to the controller.
	wire [2:0] colour;
	wire [6:0] x;
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
			
	// Put your code here. Your code should produce signals x,y,colour and writeEn/plot
	// for the VGA controller, in addition to any other functionality your design may require.
    
    // Instansiate datapath
	// datapath d0(...);
	

    // Instansiate FSM control
    // control c0(...);
	combination c0(
		.clk(CLOCK_50),
		.resetn(resetn),
		.start(start),
		.sig_left(~KEY[3]),
		.sig_right(~KEY[2]),
		.position_x(x),
		.position_y(y),
		.color_out(colour),
		.plot(writeEn)
		);
	 
	 
	 
endmodule


// Problem to fix:
//  random
//  move left, move right


module combination(
	input clk,
	input resetn,
	input start,
	input sig_left, sig_right,
	
	output [6:0] position_x, position_y,
	output [2:0] color_out,
	output plot
	);
	
	wire [1:0] add_x, add_y;
	wire [1:0] select;
	wire move_down, move_left, move_right;
	wire [13:0] pos_indicator1, pos_indicator2, pos_indicator3, pos_indicator4;
	wire [13:0] position_out;
	wire new_piece;
	wire [2:0] shape_indicator;
	assign position_x = position_out[13:7];
	assign position_y = position_out[6:0];
	
	
	datapath d0(
		.add_x(add_x),
		.add_y(add_y),
		.clk(clk),
		.resetn(resetn),
		.draw(draw),
		.select(select),
		.move_down(move_down),
		.move_left(move_left),
		.move_right(move_right),
		.new_piece(new_piece),
		.position_out(position_out),
		.color_out(color_out),
		.pos_indicator1(pos_indicator1),
		.pos_indicator2(pos_indicator2),
		.pos_indicator3(pos_indicator3),
		.pos_indicator4(pos_indicator4),
		.shape_indicator(shape_indicator)
		);
		
	control c0(
		.clk(clk),
		.resetn(resetn),
		.start(start),
		.current_pos1(pos_indicator1),
		.current_pos2(pos_indicator2),
		.current_pos3(pos_indicator3),
		.current_pos4(pos_indicator4),
		.shape_indicator(shape_indicator),
		.sig_left(sig_left),
		.sig_right(sig_right),
		.add_x(add_x),
		.add_y(add_y),
		.block_counter(select),
		.draw(draw),
		.plot(plot),
		.move_down(move_down),
		.move_left(move_left),
		.move_right(move_right),
		.new_piece(new_piece)
		);
endmodule


module datapath(
	input [1:0] add_x, add_y,
	input draw, resetn, clk,
	input [1:0] select,
	input move_down, move_left, move_right,// signal to let the x and y registers store the position of four blocks
	input new_piece, // signal to drop the new piece
	output reg [13:0] position_out,
	output reg [2:0] color_out,
	output [13:0] pos_indicator1, pos_indicator2, pos_indicator3, pos_indicator4,
	output [2:0] shape_indicator
	);
	
	//input registers
	reg [13:0] p1, p2, p3, p4; 
	
	// random unit
	reg [2:0] random;
	// random color unit
	reg [2:0] random_color;
	
	// color reg
	reg [2:0] color;
	
	
	// need a shape indicator
	assign shape_indicator = random;
	
	
	always @(posedge clk) begin
		if (!resetn)
			random <= 0;
		else 
			if (random == 3'b111)
				random <= 0;
			else 
				random <= random + 1'b1;
	end
	
	always @(posedge clk) begin
		if (!resetn)
			random_color <= 3'b001;
		else if (new_piece)
			if (random_color == 3'b111)
				random_color <= 3'b001;
			else 
				random_color <= random_color + 1'b1;
	end
	

	// shape of blocks
	localparam square_shape 	 = 8'd0,
				  I_shape      	 = 8'd1,
				  l_I_shape    	 = 8'd2,
				  r_I_shape     	 = 8'd3,
				  S_shape      	 = 8'd4,
				  Z_shape      	 = 8'd5,
				  r_horizontal_shape = 8'd6,
				  l_horizontal_shape = 8'd7;
	
	always @(posedge clk) begin
		if (!resetn) begin 
			p1 <= 14'b10100000101000;    
			p2 <= 14'b10101000101000;
			p3 <= 14'b10100000101100;
			p4 <= 14'b10101000101100;
		end
		else if (new_piece) begin
			if (random == square_shape) begin  // The first piece is a square 
				p1 <= 14'b1010000_0101000;   // (80, 40)
				p2 <= 14'b1010100_0101000;   //
				p3 <= 14'b1010000_0101100;   //
				p4 <= 14'b1010100_0101100;	  //		
			end
			else if (random == I_shape) begin
				p1 <= 14'b1010000_0101000;
				p2 <= 14'b1010000_0101100;
				p3 <= 14'b1010000_0110000;
				p4 <= 14'b1010000_0110100;
			end
			else if (random == l_I_shape) begin
				p1 <= 14'b1010000_0101000;
				p2 <= 14'b1001100_0101100;
				p3 <= 14'b1010000_0101100;
				p4 <= 14'b1010000_0110000;
			end
			else if (random == r_I_shape) begin
				p1 <= 14'b1010000_0101000;
				p2 <= 14'b1010100_0101100;	
				p3 <= 14'b1010000_0101100;
				p4 <= 14'b1010000_0110000;
			end
			else if (random == S_shape) begin
				p1 <= 14'b1010000_0101000; // (80,40)
				p2 <= 14'b1001100_0101000;	// (76,40)
				p3 <= 14'b1001100_0101100; // (76,44)
				p4 <= 14'b1001000_0101100; // (72,44)
			end
			else if (random == Z_shape) begin
				p1 <= 14'b1010000_0101000; // (80,40)
				p2 <= 14'b1010100_0101000;	// (84,40)
				p3 <= 14'b1010100_0101100; // (84,44)
				p4 <= 14'b1011000_0101100;	// (88,44)
			end
			else if (random == r_horizontal_shape) begin
				p1 <= 14'b1010000_0101000; // (80, 40)
				p2 <= 14'b1010000_0101100;	// (80, 44)
				p3 <= 14'b1010100_0101100; // (84, 44)
				p4 <= 14'b1011000_0101100;	// (88, 44)
			end
			else if (random == l_horizontal_shape) begin 
				p1 <= 14'b1010000_0101000; // (80, 40)
				p2 <= 14'b1010000_0101100;	// (80, 44)
				p3 <= 14'b1001100_0101100; // (76, 44)
				p4 <= 14'b1001000_0101100;	// (72, 44)
			end
		end
		else begin
			if (move_down) begin // move_down case
				p1[6:0] <= p1[6:0] + 3'b100;
				p2[6:0] <= p2[6:0] + 3'b100;
				p3[6:0] <= p3[6:0] + 3'b100;
				p4[6:0] <= p4[6:0] + 3'b100;
			end
		   else if (move_left) begin
				if (p1[13:7] > 7'b0111100 && p2[13:7] > 7'b0111100 && p3[13:7] > 7'b0111100 && p4[13:7] > 7'b0111100) begin
					p1[13:7] <= p1[13:7] - 3'b100;
					p2[13:7] <= p2[13:7] - 3'b100;
					p3[13:7] <= p3[13:7] - 3'b100;
					p4[13:7] <= p4[13:7] - 3'b100;
				end
			end
			else if (move_right) begin
				if (p1[13:7] < 7'b1100100 && p2[13:7] < 7'b1100100 && p3[13:7] < 7'b1100100 && p4[13:7] < 7'b1100100) begin
					p1[13:7] <= p1[13:7] + 3'b100;
					p2[13:7] <= p2[13:7] + 3'b100;
					p3[13:7] <= p3[13:7] + 3'b100;
					p4[13:7] <= p4[13:7] + 3'b100;
				end
			end
		end
	end
	
	always @(posedge clk) begin
		if (!resetn) 
			color <= 3'b000;
		else begin
			if (new_piece)
				color <= random_color;
		end
	
	end
	
	always @(*) begin
		if (draw)
			color_out = color;
		else 
			color_out = 3'b000;
	end
	
	wire [13:0] p1_out, p2_out, p3_out, p4_out;
	assign p1_out = {p1[13:7] + add_x, p1[6:0] + add_y};
	assign p2_out = {p2[13:7] + add_x, p2[6:0] + add_y};
	assign p3_out = {p3[13:7] + add_x, p3[6:0] + add_y};
	assign p4_out = {p4[13:7] + add_x, p4[6:0] + add_y};
	
	always @(*) 
	begin 
		if (select == 0)
			position_out = p1_out;
		else if (select == 1)
			position_out = p2_out;
		else if (select == 2)
		   position_out = p3_out;
		else if (select == 3)
			position_out = p4_out;
		else 
			position_out = 0;
	end
	
	assign pos_indicator1 =   p1;
	assign pos_indicator2 =   p2;
	assign pos_indicator3 =   p3;
	assign pos_indicator4 =   p4;
endmodule



module control(
	input clk, resetn,
	input start,
	input [13:0] current_pos1, current_pos2, current_pos3, current_pos4,
	input sig_left, sig_right,
	input [2:0] shape_indicator,
	
	output reg [1:0] add_x, add_y, 
	output reg [1:0] block_counter,
	output reg draw,
	output reg plot,
	output reg move_down, move_left, move_right,
	output reg new_piece
	);
	
	reg [3:0] pos_add_counter;
	reg [3:0] current_state, next_state;
	
	reg [24:0] delay_counter;
	
	reg reg_left, reg_right;
	
	// signal to update the game board and signal to clear the game board
	reg clear;
	reg update;
	
	// This is the whole game board.
	reg [9:0] row [0:19];
	integer index;
	
	
	localparam S_START                = 4'd0,
				  S_START_WAIT           = 4'd1,
				  S_NEW_PIECE            = 4'd2,
				  S_COLLISION_CHECK_1    = 4'd3,
				  S_DRAW                 = 4'd4,
				  S_DRAW_WAIT            = 4'd5,
				  S_COLLISION_CHECK_2    = 4'd6,
				  S_UPDATE               = 4'd7,
				  S_ERASE                = 4'd8,
				  S_MOVE                 = 4'd9,
				  S_OVER                 = 4'd10,
				  S_OVER_WAIT            = 4'd11;
				  
	// The delay suppose to be 0.5s  25'b1011111010111100001000000
	// FSM			  
	always @(*) begin
		case(current_state)
			S_START: next_state = start ? S_START_WAIT : S_START; // need to clean everthing on memory and screen
			S_START_WAIT: next_state = start? S_START_WAIT: S_NEW_PIECE;
			S_NEW_PIECE: next_state = S_COLLISION_CHECK_1;
			S_COLLISION_CHECK_1: begin // if failed, we go to game over, this collision mainly depend on the shape_indicator
				if (shape_indicator == 3'b000)      // square shape
					next_state = (row[0][5] || row[0][6] || row[1][5] || row[1][6]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b001)  // I_shape
					next_state = (row[0][5] || row[1][5] || row[2][5] || row[3][5]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b010) // l_I_shape
					next_state = (row[0][5] || row[1][5] || row[1][4] || row[2][5]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b011) // r_I_shape
					next_state = (row[0][5] || row[1][5] || row[1][6] || row[2][5]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b100) // S_shape
					next_state = (row[0][5] || row[0][4] || row[1][4] || row[1][3]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b101) // Z_shape
					next_state = (row[0][5] || row[0][6] || row[1][6] || row[1][7]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b110) // r_horizontal_shape
					next_state = (row[0][5] || row[1][5] || row[1][6] || row[1][7]) ? S_OVER : S_DRAW;
				else if (shape_indicator == 3'b111) // l_horizontal_shape
					next_state = (row[0][5] || row[1][5] || row[1][4] || row[1][3]) ? S_OVER : S_DRAW;
			end
			S_DRAW: next_state = (block_counter == 2'b11 && pos_add_counter == 4'b1111) ? S_DRAW_WAIT: S_DRAW;
			S_DRAW_WAIT: next_state = (delay_counter == 25'b1011111010111100001000000) ? S_COLLISION_CHECK_2 : S_DRAW_WAIT;
			S_COLLISION_CHECK_2: begin  // if we reach the bottom of the game board, or a block is below the piece, then collision is meet
				if (current_pos4[6:0] == 7'b1110100) // This means the very bottom block of our piece is at 116 y-coordinates
					next_state = S_UPDATE;
				else if (row[((current_pos1[6:0] - 7'd40) >> 2) + 1'b1][(current_pos1[13:7] - 7'd60) >> 2] == 1 ||    // not at the very bottom, so check if there is block below it
							row[((current_pos2[6:0] - 7'd40) >> 2) + 1'b1][(current_pos2[13:7] - 7'd60) >> 2] == 1 ||
							row[((current_pos3[6:0] - 7'd40) >> 2) + 1'b1][(current_pos3[13:7] - 7'd60) >> 2] == 1 ||
							row[((current_pos4[6:0] - 7'd40) >> 2) + 1'b1][(current_pos4[13:7] - 7'd60) >> 2] == 1)   																																					
					next_state = S_UPDATE;
				else   // no collision in this case
					next_state = S_ERASE;
			end
			S_UPDATE: next_state = S_NEW_PIECE;
			S_ERASE: next_state = (block_counter == 2'b11 && pos_add_counter == 4'b1111) ? S_MOVE : S_ERASE;
			S_MOVE: next_state = S_DRAW;
			S_OVER: next_state = start ? S_OVER_WAIT : S_OVER;
			S_OVER_WAIT: next_state = start ? S_OVER_WAIT : S_START;  
			default: next_state = S_START;
		endcase
	end
	
	

	
	
	// current state registers
	always @(posedge clk) begin
		  if(!resetn)
				current_state <= S_START;
		  else
				current_state <= next_state;
	end // state_FFS
	 
	// Output logic aka all of our datapath control signals
	always @(*) begin 
		// by default make all of signals 0
		add_x = 0;
		add_y = 0;
		draw = 0;
		plot = 0;
		move_down = 0;
		new_piece = 0;
		move_left = 0;
		move_right = 0;
		update = 0;
		clear = 0;
		
		case(current_state) 
			S_START: begin
				clear = 1;
			end
			S_NEW_PIECE: begin
				new_piece = 1;
			end
			
			S_DRAW: begin
				draw = 1;
				plot = 1;
				add_x <= pos_add_counter[3:2];
				add_y <= pos_add_counter[1:0];
			end
			
			S_UPDATE: begin
				update = 1;
			end
			S_ERASE: begin
				plot = 1;
				add_x <= pos_add_counter[3:2];
				add_y <= pos_add_counter[1:0];
			end
			S_MOVE: begin
				if (sig_left && (row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) - 1'b1] == 0 &&
				                 row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) - 1'b1] == 0 &&
								     row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) - 1'b1] == 0 &&
								     row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) - 1'b1] == 0)) begin // left side collision check
					move_left = 1;
				end
				else if (sig_right && (row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) + 1'b1] == 0 &&
				                       row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) + 1'b1] == 0 &&
										     row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) + 1'b1] == 0 &&
										     row[(current_pos1[6:0] - 7'd40) >> 2][((current_pos1[13:7] - 7'd60) >> 2) + 1'b1] == 0)) begin
					move_right = 1;
				end
				else 
					move_down = 1;
			end
			
		endcase
	end
	
	

	
	// This counter is responsible for drawing 16 pixels (1 block)
	always @(posedge clk) begin
		if (!resetn) 
			pos_add_counter <= 4'b0000;
		else if (current_state == S_DRAW || current_state == S_ERASE)
			begin
				if(pos_add_counter == 4'b1111)
					pos_add_counter <= 4'b0000;
				else
					pos_add_counter <= pos_add_counter + 1'b1;
			end
	end
	
	// This counter is responsible for drawing 4 blocks
	always @(posedge clk) 
	begin
		if (!resetn) 
			block_counter <= 2'b00;
		else if (current_state == S_DRAW || current_state == S_ERASE)
			begin 
				if (block_counter== 2'b11 && pos_add_counter == 4'b1111)
					block_counter <= 2'b00;
				else if (pos_add_counter == 4'b1111)
					block_counter <= block_counter + 1'b1;	
					
					
			end
	end
	
	//This is a rate divider for 0.5 seconds
	always @(posedge clk)
	begin 
		if (!resetn)
			delay_counter <= 0;
		else if (current_state == S_DRAW_WAIT) begin
			if (delay_counter == 25'b1011111010111100001000000)
				delay_counter <= 0;
			else 
				delay_counter <= delay_counter + 1'b1;
		end
	end
	
	always @(posedge clk)
	begin 
		if (!resetn)
			for (index = 0; index < 20; index=index+1) begin
				row[index] <= 10'd0;
			end
		else if (clear)
			for (index = 0; index < 20; index=index+1) begin
				row[index] <= 10'd0;
			end
		else if (update) begin
			row[(current_pos1[6:0] - 7'd40) >> 2][(current_pos1[13:7] - 7'd60) >> 2] <= 1;
			row[(current_pos2[6:0] - 7'd40) >> 2][(current_pos2[13:7] - 7'd60) >> 2] <= 1;     // before we go to new_piece_state, we need to update in main_memory
			row[(current_pos3[6:0] - 7'd40) >> 2][(current_pos3[13:7] - 7'd60) >> 2] <= 1;
			row[(current_pos4[6:0] - 7'd40) >> 2][(current_pos4[13:7] - 7'd60) >> 2] <= 1;	
		end
	end
	
	
	
	

endmodule

