module mux4to1(u, v, w, x, s1, s0, m);
	input u; //selected when s1 is 0 and s0 is 0
	input v; //selected when s1 is 0 and s0 is 1
	input w; //selected when s1 is 1 and s0 is 0
	input x; //selected when s1 is 1 and s0 is 1
	input s1,s0; //select signal
	output m;
	
	wire Connection1, Connection2;
	
	mux2to1 m1(u,v,s0,Connection1);
	mux2to1 m2(w,x,s0,Connection2);
	mux2to1 m3(Connection1,Connection2,s1,m);

endmodule 

module mux2to1(x, y, s, m);
	input x; //selected when s is 0
	input y; //selected when s is 1
	input s; //select signal
	output m; //output
	
	assign m = s & y | ~s & x;
	
endmodule

