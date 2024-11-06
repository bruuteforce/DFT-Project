`timescale 1ns/1ns
`include "test_ckt.v"

module testbench;

	reg A,B,C,D,E,F;
	wire Z;

	test_ckt uut (Z,A,B,C,D,E,F);
	
	initial begin
		$display("A,B,C,D,E,F,g,h,k,l,m,p,q,s,r,u,w,Z");
		$monitor("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",A,B,C,D,E,F,uut.g,uut.h,uut.k,uut.l,uut.m,uut.p,uut.q,uut.s,uut.r,uut.u,uut.w,Z);
		for (integer i = 0; i < 64; i = i + 1) begin 
			{A, B, C, D, E, F} = i; 
			#1;
		end
		
	end

endmodule