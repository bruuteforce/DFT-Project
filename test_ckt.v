module test_ckt(Z,A,B,C,D,E,F);
	input A,B,C,D,E,F;
	output Z;
	
	wire g,h,k,l,m,p,q,s,r,u,w;

	or OR2_1 (g,C,D);
	and AND2_2 (h,C,g);
	and AND2_3 (k,g,D);
	or OR2_4 (m,h,k);
	xor XOR2_5 (l,E,F);
	nor NOR3_6 (p,A,B,m);
	or OR2_7 (q,m,B);
	or OR2_8 (s,B,l);
	and AND2_9 (r,A,p);
	and AND2_10 (u,A,m);
	and AND2_11 (w,q,s);
	xor XOR3_12 (Z,r,u,w);
	
endmodule	
