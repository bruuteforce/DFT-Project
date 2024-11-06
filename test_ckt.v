module test_ckt(Z,A,B,C,D,E,F);
	input A,B,C,D,E,F;
	output Z;
	
	wire g,h,k,l,m,p,q,s,r,u,w;

	or G1 (g,C,D);
	and G2 (h,C,g);
	and G3 (k,g,D);
	or G4 (m,h,k);
	xor G5 (l,E,F);
	nor G6 (p,A,B,m);
	or G7 (q,m,B);
	or G8 (s,B,l);
	and G9 (r,A,p);
	and G10 (u,p,m);
	and G11 (w,q,s);
	xor G12 (Z,r,u,w);
	
endmodule	
