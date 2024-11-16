import pandas as pd
import os
import re 
from itertools import product
from sample_ckt import sample_circuit
from c432 import evaluate_c432

Out_File="Results_ATPG.txt"
with open(Out_File, 'w') as f:
    pass



def worker(ckt,fault="A/STF",outputs=["Z"],inputs=["A","B","C","D","E","F"]):
    parts = fault.split('/')
    wire=parts[0]
    V1_wire=None
    V2_wire=None
    match(parts[1]):
        case("STR"):
            V1_wire=0
            V2_wire=1
        case("STF"):
            V1_wire=1
            V2_wire=0
        case _:
            print("Invalid case!")
    print(V1_wire,V2_wire,wire)
    test_patterns = []
    for inputs in product([0, 1], repeat=len(Inputs)):  
        wire_val, *outs = ckt(inputs, wire)
        outs_list=list(outs)
        for Z in outs_list:
            print(inputs,wire_val,outs_list)
            if (wire_val == V1_wire) and (len(test_patterns) == 0): 
                test_patterns.append((inputs, wire_val, Z))
            elif wire_val == V2_wire and Z == V2_wire and (len(test_patterns) == 1):  
                test_patterns.append((inputs, wire_val, Z))
            if len(test_patterns) == 2:  # Stop once we have two patterns
                break
    print("Test Patterns:")
    for i, (inputs, wire_val, output) in enumerate(test_patterns, 1):
        print(f"Pattern {inputs} -> {wire_val}, {output}")
    
    # with open(Out_File, 'a') as f:
    #     print("Test Vectors for fault:",fault)
    #     f.write(f"Test Vectors for fault:{fault}\n")
    # if not pairs:
    #     with open(Out_File, 'a') as f:
    #         print(f"Fault Not Detected.")
    #         f.write(f"\tFault Not Detected.\n")
    # else:
    #     for pair in pairs:
    #         with open(Out_File, 'a') as f:
    #             row_str = ' '.join([f"{col}" for col, val in tt.iloc[pair[0]].items()]) 
    #             print(f"[{row_str}]")
    #             f.write(f"\t[{row_str}]\n")
    #             row_str = ' '.join([f"{val}" for col, val in tt.iloc[pair[0]].items()]) 
    #             print(f"[{row_str}]")
    #             f.write(f"V1:\t[{row_str}]\n")
    #             row_str = ' '.join([f"{val}" for col, val in tt.iloc[pair[1]].items()]) 
    #             print(f"[{row_str}]")
    #             f.write(f"V2:\t[{row_str}]\n")
    #         break 

def read_verilog_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def parse_verilog(file_content):

    mod_name_pattern = re.compile(r'\bmodule\s+(\w+)\s*\(', re.IGNORECASE) 
    match = mod_name_pattern.search(file_content)

    module_pattern = re.compile(r'module\s+\w+\s*\((.*?)\);', re.DOTALL)
    input_pattern = re.compile(r'input\s+(.*?);', re.DOTALL)
    output_pattern = re.compile(r'output\s+(.*?);', re.DOTALL)
    wire_pattern = re.compile(r'wire\s+(.*?);', re.DOTALL)

    module_match = module_pattern.search(file_content)
    input_match = input_pattern.search(file_content)
    output_match = output_pattern.search(file_content)
    wire_match = wire_pattern.search(file_content)
    
    inputs = []
    outputs = []
    wires = []
    mod_ports = []

    if module_match:
        module_ports = module_match.group(1).split(',') 
        mod_ports.extend([port.strip() for port in module_ports])
                                                                         
    if input_match:
        input_ports = input_match.group(1).split(',')
        inputs.extend([port.strip() for port in input_ports])
    
    if output_match:
        output_ports = output_match.group(1).split(',')
        outputs.extend([port.strip() for port in output_ports])
    
    if wire_match:
        wire_ports = wire_match.group(1).split(',')
        wires.extend([port.strip() for port in wire_ports])
    
    return  match.group(1), inputs, outputs, wires, mod_ports

def generate_testbench(module_name, ckt, mod_ports, inputs, outputs,wires,v_file):
    monitor_vars = inputs + [f"uut.{wire}" for wire in wires] + outputs
    monitor_format = ",".join(["%d"] * len(monitor_vars))
    monitor_vars_str = ",".join(monitor_vars)
    monitor_string = f'$monitor("{monitor_format}", {monitor_vars_str});'
    total_input_combinations=pow(2,len(inputs))
    tb_content = f"""
`timescale 1ns/1ns
`include "{v_file}"

module {module_name}_tb;

reg {', '.join(inputs)};
wire {', '.join(outputs)};

{ckt} uut (
    {', '.join(mod_ports)}
);

	initial begin
		$display("{','.join(inputs)},{','.join(wires)},{','.join(outputs)}");
		{monitor_string}
		for (integer i = 0; i < {total_input_combinations}; i = i + 1) begin 
			{'{'+", ".join(inputs)+'}'} = i; 
			#1;
		end
		
	end

endmodule
"""
    return tb_content

v_file="E:\DFT\project\\c432.v"

# Read the Verilog file content
verilog_content = read_verilog_file(v_file)

# Continue with parsing the Verilog content
ckt_name, Inputs, Outputs, Wires, Mod_ports = parse_verilog(verilog_content)

print(f"Inputs: {Inputs}")
print(f"Outputs: {Outputs}")
print(f"Wires: {Wires}")

#testbench_content=generate_testbench("testbench",ckt_name,Mod_ports,Inputs,Outputs,Wires,v_file)
#with open(f"testbench.v", 'w') as tb_file:
#    tb_file.write(testbench_content)

#os.system(f"C:\iverilog\\bin\iverilog.exe -I E:\DFT\project\ -o TB E:\DFT\project\\testbench.v")   
#os.system(f"C:\iverilog\\bin\\vvp.exe -l TT.csv TB")  

####################################################
#Fault_List=["A/STR","B/STR","C/STR","D/STR","E/STR","F/STR","g/STR","h/STR","k/STR","l/STR","m/STR","p/STR","q/STR","s/STR","r/STR","u/STR","w/STR","Z/STR","A/STF","B/STF","C/STF","D/STF","E/STF","F/STF","g/STF","h/STF","k/STF","l/STF","m/STF","p/STF","q/STF","s/STF","r/STF","u/STF","w/STF","Z/STF"]
#Inputs=["A","B","C","D","E","F"]
#Outputs=["Z"]
Fault_List=["N1/STR"]
for fault in Fault_List:
    worker(evaluate_c432,fault,Outputs,Inputs)