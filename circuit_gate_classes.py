from itertools import product
from parse_ckt import parse_file
from sync_basics import parse_verilog
from sync_basics import read_verilog_file
import copy

def custom_and(*args):
    result = 1  # Start with True
    for arg in args:
        if arg == 0:
            return 0  # AND with 0 results in 0
        if arg is None:
            result = None  # None propagates but doesn't force 0
    return result

def custom_or(*args):
    result = 0  # Start with False
    for arg in args:
        if arg == 1:
            return 1  # OR with 1 results in 1
        if arg is None and result == 0:
            result = None  # None propagates if there's no 1
    return result

def custom_not(arg):
    if arg == 0:
        return 1
    if arg == 1:
        return 0
    return None

def custom_nand(*args):
    and_result = custom_and(*args)
    return custom_not(and_result)

def custom_nor(*args):
    or_result = custom_or(*args)
    return custom_not(or_result)

def custom_xor(*args):
    result = 0
    none_count = 0
    for arg in args:
        if arg is None:
            none_count += 1
        else:
            result ^= arg
    if none_count > 0:
        return None
    return result

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
        # inputs = [faults.get(inp, values.get(inp, 0)) if values.get(inp) is not None else 0 for inp in self.inputs]
        inputs = [faults.get(inp, values.get(inp)) for inp in self.inputs]
        if self.operation == 'OR' or self.operation == 'OR2':
            #self.output_value = inputs[0] | inputs[1]
            self.output_value = custom_or(inputs[0],inputs[1])
        elif self.operation == 'AND' or self.operation == 'AND2':
            # self.output_value = inputs[0] & inputs[1]
            self.output_value = custom_and(inputs[0],inputs[1])
        elif self.operation == 'XOR' or self.operation == 'XOR2':
            # self.output_value = inputs[0] ^ inputs[1]
            self.output_value = custom_xor(inputs[0],inputs[1])
        elif self.operation == 'NOR' or self.operation == 'NOR2':
            # self.output_value = int(not (inputs[0] | inputs[1]))
            self.output_value = custom_nor(inputs[0],inputs[1])
        elif self.operation == 'NOR3':
            # self.output_value = int(not (inputs[0] | inputs[1] | inputs[2]))
            self.output_value = custom_nor(inputs[0],inputs[1],inputs[2])
        elif self.operation == 'XOR3':
            # self.output_value = inputs[0] ^ inputs[1] ^ inputs[2]
            self.output_value = custom_xor(inputs[0],inputs[1],inputs[2])
        elif self.operation == 'NOT1':
            # self.output_value = int(not(inputs[0]))
            self.output_value = custom_not(inputs[0])
        elif self.operation == 'NAND2':
            # self.output_value = int(not(inputs[0] & inputs[1]))
            self.output_value = custom_nand(inputs[0],inputs[1])
        elif self.operation == 'AND9':
            # self.output_value = inputs[0] & inputs[1] & inputs[2] & inputs[3] & inputs[4] & inputs[5] &inputs[6] & inputs[7] & inputs[8]
            self.output_value = custom_and(inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5],inputs[6],inputs[7],inputs[8])
        elif self.operation == 'NAND4':
            # self.output_value = int(not(inputs[0] & inputs[1] & inputs[2] & inputs[3]))
            self.output_value = custom_nand(inputs[0],inputs[1],inputs[2],inputs[3])
        elif self.operation == 'AND8':
            # self.output_value = inputs[0] & inputs[1] & inputs[2] & inputs[3] & inputs[4] & inputs[5] &inputs[6] & inputs[7]
            self.output_value = custom_and(inputs[0],inputs[1],inputs[2],inputs[3], inputs[4], inputs[5], inputs[6], inputs[7])
        elif self.operation == 'NAND3':
            # self.output_value = int(not(inputs[0] & inputs[1] & inputs[2]))
            self.output_value = custom_nand(inputs[0], inputs[1], inputs[2])
        else:
            raise ValueError('Unknown operation')
        
        values[self.output] = self.output_value


class Circuit:
    def __init__(self,inputs,outputs):
        self.gates = []
        self.inputs = copy.deepcopy(inputs)
        self.outputs = copy.deepcopy(outputs)
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

    def print_outputs(self,prefix):
        dict={}
        for output in self.outputs:
            dict[output]=self.values[output]
        print(f"{prefix}{dict}")

    def print_inputs(self,prefix):
        dict={}
        for input in self.inputs:
            dict[input]=self.values[input]
        print(f"{prefix}{dict}")

    def print_faults(self):
        print(self.faults)
    
    def get_outputs(self): 
        return {output: self.values[output] for output in self.outputs}

# Define the circuit
def create_test_ckt(filename,inputs,outputs):
    circuit = Circuit(inputs,outputs)

    gates = parse_file(filename)
    for gate in gates:
        # print(gate)
        circuit.add_gate(Gate(gate['gate_name'],gate['gate'],gate['inputs'],gate['output']))

    return circuit
def inject_fault(circuit, fault):
    fault_type, fault_location = fault
    circuit.inject_fault(fault_type, fault_location)

def check_fault_loc_value(circuit,fault,idx=0):
    fault_type, fault_location = fault
    # print(f"{idx}::{fault_location},{fault_type},{circuit.get_output(fault_location)}")
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

