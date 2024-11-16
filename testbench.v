
`timescale 1ns/1ns
`include "E:\DFT\project\c432.v"

module testbench_tb;

reg N1, N4, N8, N11, N14, N17, N21, N24, N27, N30, N34, N37, N40, N43, N47, N50, N53, N56, N60, N63, N66, N69, N73, N76, N79, N82, N86, N89, N92, N95, N99, N102, N105, N108, N112, N115;
wire N223, N329, N370, N421, N430, N431, N432;

c432 uut (
    N1, N4, N8, N11, N14, N17, N21, N24, N27, N30, N34, N37, N40, N43, N47, N50, N53, N56, N60, N63, N66, N69, N73, N76, N79, N82, N86, N89, N92, N95, N99, N102, N105, N108, N112, N115, N223, N329, N370, N421, N430, N431, N432
);

	initial begin
		$display("N1,N4,N8,N11,N14,N17,N21,N24,N27,N30,N34,N37,N40,N43,N47,N50,N53,N56,N60,N63,N66,N69,N73,N76,N79,N82,N86,N89,N92,N95,N99,N102,N105,N108,N112,N115,N118,N119,N122,N123,N126,N127,N130,N131,N134,N135,N138,N139,N142,N143,N146,N147,N150,N151,N154,N157,N158,N159,N162,N165,N168,N171,N174,N177,N180,N183,N184,N185,N186,N187,N188,N189,N190,N191,N192,N193,N194,N195,N196,N197,N198,N199,N203,N213,N224,N227,N230,N233,N236,N239,N242,N243,N246,N247,N250,N251,N254,N255,N256,N257,N258,N259,N260,N263,N264,N267,N270,N273,N276,N279,N282,N285,N288,N289,N290,N291,N292,N293,N294,N295,N296,N300,N301,N302,N303,N304,N305,N306,N307,N308,N309,N319,N330,N331,N332,N333,N334,N335,N336,N337,N338,N339,N340,N341,N342,N343,N344,N345,N346,N347,N348,N349,N350,N351,N352,N353,N354,N355,N356,N357,N360,N371,N372,N373,N374,N375,N376,N377,N378,N379,N380,N381,N386,N393,N399,N404,N407,N411,N414,N415,N416,N417,N418,N419,N420,N422,N425,N428,N429,N223,N329,N370,N421,N430,N431,N432");
		$monitor("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d", N1,N4,N8,N11,N14,N17,N21,N24,N27,N30,N34,N37,N40,N43,N47,N50,N53,N56,N60,N63,N66,N69,N73,N76,N79,N82,N86,N89,N92,N95,N99,N102,N105,N108,N112,N115,uut.N118,uut.N119,uut.N122,uut.N123,uut.N126,uut.N127,uut.N130,uut.N131,uut.N134,uut.N135,uut.N138,uut.N139,uut.N142,uut.N143,uut.N146,uut.N147,uut.N150,uut.N151,uut.N154,uut.N157,uut.N158,uut.N159,uut.N162,uut.N165,uut.N168,uut.N171,uut.N174,uut.N177,uut.N180,uut.N183,uut.N184,uut.N185,uut.N186,uut.N187,uut.N188,uut.N189,uut.N190,uut.N191,uut.N192,uut.N193,uut.N194,uut.N195,uut.N196,uut.N197,uut.N198,uut.N199,uut.N203,uut.N213,uut.N224,uut.N227,uut.N230,uut.N233,uut.N236,uut.N239,uut.N242,uut.N243,uut.N246,uut.N247,uut.N250,uut.N251,uut.N254,uut.N255,uut.N256,uut.N257,uut.N258,uut.N259,uut.N260,uut.N263,uut.N264,uut.N267,uut.N270,uut.N273,uut.N276,uut.N279,uut.N282,uut.N285,uut.N288,uut.N289,uut.N290,uut.N291,uut.N292,uut.N293,uut.N294,uut.N295,uut.N296,uut.N300,uut.N301,uut.N302,uut.N303,uut.N304,uut.N305,uut.N306,uut.N307,uut.N308,uut.N309,uut.N319,uut.N330,uut.N331,uut.N332,uut.N333,uut.N334,uut.N335,uut.N336,uut.N337,uut.N338,uut.N339,uut.N340,uut.N341,uut.N342,uut.N343,uut.N344,uut.N345,uut.N346,uut.N347,uut.N348,uut.N349,uut.N350,uut.N351,uut.N352,uut.N353,uut.N354,uut.N355,uut.N356,uut.N357,uut.N360,uut.N371,uut.N372,uut.N373,uut.N374,uut.N375,uut.N376,uut.N377,uut.N378,uut.N379,uut.N380,uut.N381,uut.N386,uut.N393,uut.N399,uut.N404,uut.N407,uut.N411,uut.N414,uut.N415,uut.N416,uut.N417,uut.N418,uut.N419,uut.N420,uut.N422,uut.N425,uut.N428,uut.N429,N223,N329,N370,N421,N430,N431,N432);
		for (integer i = 0; i < 68719476736; i = i + 1) begin 
			{N1, N4, N8, N11, N14, N17, N21, N24, N27, N30, N34, N37, N40, N43, N47, N50, N53, N56, N60, N63, N66, N69, N73, N76, N79, N82, N86, N89, N92, N95, N99, N102, N105, N108, N112, N115} = i; 
			#1;
		end
		
	end

endmodule
