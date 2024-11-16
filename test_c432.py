from itertools import product
import re
from c432 import evaluate_c432


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


v_file="E:\DFT\project\\c432.v"

# Read the Verilog file content
verilog_content = read_verilog_file(v_file)

# Continue with parsing the Verilog content
ckt_name, Inputs, Outputs, Wires, Mod_ports = parse_verilog(verilog_content)

print(f"Inputs: {Inputs}")
print(f"Outputs: {Outputs}")
print(f"Wires: {Wires}")


for inputs in product([0, 1], repeat=len(Inputs)):
    out = evaluate_c432(inputs,'N1')
    print(inputs,out)