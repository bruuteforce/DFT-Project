from itertools import product
from parse_ckt import parse_file
from Sync_Icarus_extended import parse_verilog
from Sync_Icarus_extended import read_verilog_file

import random

def random_sampling(n_inputs, n_samples):
    return [tuple(random.randint(0, 1) for _ in range(n_inputs)) for _ in range(n_samples)]

# Example: Generate 1000 random samples for a 36-input circuit
test_patterns = random_sampling(36, 1000)

class Gate:
    def __init__(self, name, operation, inputs, output):
        self.name = name
        self.operation = operation
        self.inputs = inputs
        self.output = output

    def evaluate(self, values, faults):
        # Apply the fault if it affects this gate's output
        if self.output in faults:
            values[self.output] = faults[self.output]
            return
        inputs = [faults.get(inp, values[inp]) for inp in self.inputs]
        if self.operation == 'OR':
            self.output_value = inputs[0] | inputs[1]
        elif self.operation == 'AND':
            self.output_value = inputs[0] & inputs[1]
        elif self.operation == 'XOR' or self.operation == 'XOR2':
            self.output_value = inputs[0] ^ inputs[1]
        elif self.operation == 'NOR' or self.operation == 'NOR2':
            self.output_value = int(not (inputs[0] | inputs[1]))
        elif self.operation == 'NOR3':
            self.output_value = int(not (inputs[0] | inputs[1] | inputs[2]))
        elif self.operation == 'XOR3':
            self.output_value = inputs[0] ^ inputs[1] ^ inputs[2]
        elif self.operation == 'NOT1':
            self.output_value = int(not(inputs[0]))
        elif self.operation == 'NAND2':
            self.output_value = int(not(inputs[0] & inputs[1]))
        elif self.operation == 'AND9':
            self.output_value = inputs[0] & inputs[1] & inputs[2] & inputs[3] & inputs[4] & inputs[5] &inputs[6] & inputs[7] & inputs[8]
        elif self.operation == 'NAND4':
            self.output_value = int(not(inputs[0] & inputs[1] & inputs[2] & inputs[3]))
        elif self.operation == 'AND8':
            self.output_value = inputs[0] & inputs[1] & inputs[2] & inputs[3] & inputs[4] & inputs[5] &inputs[6] & inputs[7]
        elif self.operation == 'NAND3':
            self.output_value = int(not(inputs[0] & inputs[1] & inputs[2]))
        else:
            raise ValueError('Unknown operation')
        
        values[self.output] = self.output_value


class Circuit:
    def __init__(self,inputs,outputs):
        self.gates = []
        self.inputs = inputs
        self.outputs = outputs
        self.values = {}
        self.faults = {}

    def add_gate(self, gate):
        self.gates.append(gate)

    def set_inputs(self, **kwargs):
        for inp, value in kwargs.items():
            self.values[inp] = value

    def inject_fault(self, fault_type, fault_location):
        if fault_type == 'SA0':
            self.faults[fault_location] = 0
        elif fault_type == 'SA1':
            self.faults[fault_location] = 1

    def clear_faults(self):
        self.faults = {}

    def evaluate(self):
        for gate in self.gates:
            gate.evaluate(self.values, self.faults)

    def get_output(self, output):
        return self.values[output]

    def print_outputs(self):
        list=[]
        for output in self.outputs:
            list.append(self.values[output])
        print(list)

    def print_inputs(self):
        list=[]
        for input in self.inputs:
            list.append(self.values[input])
        print(list)

    def print_faults(self):
        print(self.faults)

# Define the circuit
def create_test_ckt(filename,inputs,outputs):
    circuit = Circuit(inputs,outputs)

    gates = parse_file(filename)
    for gate in gates:
        print(gate)
        circuit.add_gate(Gate(gate['gate_name'],gate['gate'],gate['inputs'],gate['output']))

    return circuit
def inject_fault(circuit, fault):
    fault_type, fault_location = fault
    circuit.inject_fault(fault_type, fault_location)

def check_fault_loc_value(circuit,fault):
    fault_type, fault_location = fault
    # print(fault_type,circuit.get_output(fault_location))
    if fault_type == 'SA0' and circuit.get_output(fault_location) == 0:
        return 1
    elif fault_type == 'SA1' and circuit.get_output(fault_location) == 1:
        return 1
    else:
        return 0
    
def generate_test_patterns(circuit, faults, inputs, outputs):
    test_patterns1 = []
    test_patterns2 = []
    # inputs = ['A', 'B', 'C', 'D', 'E', 'F']
    # input_combinations = list(product([0, 1], repeat=len(inputs)))
    # input_combinations = test_patterns
    input_combinations = product([0, 1], repeat=len(inputs))
    for fault in faults:
        found_v1=0    
        # for input_combination in input_combinations:
        while True:
            input_combination = next(input_combinations)
            for output in outputs:
                print(f"test pattern:{input_combination}")
                circuit.set_inputs(**dict(zip(inputs, input_combination)))
                inject_fault(circuit, fault)
                circuit.print_inputs()
                circuit.evaluate()
                circuit.print_outputs()
                circuit.print_faults() 
                fault_output = circuit.get_output(output)
                circuit.clear_faults()
                circuit.print_inputs()
                circuit.evaluate()
                circuit.print_outputs()
                circuit.print_faults() 
                no_fault_output = circuit.get_output(output)

                if (not found_v1) and check_fault_loc_value(circuit,fault):
                    test_patterns1.append(input_combination)
                    found_v1=1


                if fault_output != no_fault_output:
                    test_patterns2.append((input_combination, fault))
                    break  # Found a detecting pattern, no need to check further for this fault
    
    return test_patterns1, test_patterns2

# Conversion dictionary for fault types 
fault_map = { 
    'STR': 'SA0', 
    'STF': 'SA1' 
} 
# Function to convert the list 
def convert_fault_list(delay_faults): 
    result = [] 
    for item in delay_faults: 
        var, fault = item.split('/')
        result.append((fault_map[fault], var)) 
    return result 

# Define the circuit
v_file='c432.v'

verilog_content = read_verilog_file(v_file)
ckt_name, Inputs, Outputs, Wires, Mod_ports = parse_verilog(verilog_content)
circuit = create_test_ckt(v_file,Inputs,Outputs)

#delay faults
delay_faults = ["N118/STF"]

stuck_at_faults = convert_fault_list(delay_faults)

# Generate test patterns
test_patterns1, test_patterns2 = generate_test_patterns(circuit, stuck_at_faults,Inputs,Outputs)


for p1,p2 in zip(test_patterns1,test_patterns2):
    print(f"Test pattern 1:  {p1}")
    print(f"Test pattern 2: for {p2[1]}: {p2[0]}")