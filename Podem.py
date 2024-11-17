from D_alg_copy_copy import create_test_ckt 
from D_alg_copy_copy import generate_test_patterns
from D_alg_copy_copy import convert_fault_list
from parse_ckt import parse_file
from Sync_Icarus_extended import parse_verilog
from Sync_Icarus_extended import read_verilog_file
import multiprocessing

class PODEM:
    def __init__(self, circuit):
        self.circuit = circuit

    def find_test_pattern(self, fault):
        self.circuit.clear_faults()
        self.circuit.inject_fault(fault[0], fault[1])
        
        inputs = list(self.circuit.values.keys())
        return self.recursive_podem(inputs, fault)
    
    def recursive_podem(self, inputs, fault):
        if self.check_fault_propagation(fault):
            return dict(self.circuit.values)
        
        if not inputs:
            return None
        
        input_var = inputs.pop(0)
        
        # Try setting the input to 0
        self.circuit.set_inputs(**{input_var: 0})
        if self.recursive_podem(inputs.copy(),fault):
            return dict(self.circuit.values)
        
        # Try setting the input to 1
        self.circuit.set_inputs(**{input_var: 1})
        if self.recursive_podem(inputs.copy(),fault):
            return dict(self.circuit.values)
        
        # Restore the input value and backtrack
        self.circuit.values[input_var] = None
        return None
    
    def check_fault_propagation(self, fault):
        print("check:")
        self.circuit.inject_fault(fault[0], fault[1])
        self.circuit.evaluate()
        self.circuit.print_inputs()
        self.circuit.print_outputs()
        fault_outputs = self.circuit.get_outputs()
        
        self.circuit.clear_faults()
        self.circuit.evaluate()
        self.circuit.print_inputs()
        self.circuit.print_outputs()
        no_fault_outputs = self.circuit.get_outputs()
        
        for output in self.circuit.outputs: 
            if fault_outputs[output] is None or no_fault_outputs[output] is None: 
                return False 
            # Check if any output is different 
            if fault_outputs[output] != no_fault_outputs[output]: 
                return True
        return False



# Define the circuit
v_file='c432.v'

verilog_content = read_verilog_file(v_file)
ckt_name, Inputs, Outputs, Wires, Mod_ports = parse_verilog(verilog_content)
circuit = create_test_ckt(v_file,Inputs,Outputs)
# Initialize PODEM
podem = PODEM(circuit)
#delay faults
delay_faults = ["N381/STF"]

stuck_at_faults = convert_fault_list(delay_faults)

# Generate test patterns
#test_patterns1, test_patterns2 = generate_test_patterns(circuit, stuck_at_faults,Inputs,Outputs)


#for p1,p2 in zip(test_patterns1,test_patterns2):
#    print(f"Test pattern 1:  {p1}")
#    print(f"Test pattern 2: for {p2[1]}: {p2[0]}")

stop_event = multiprocessing.Event()

for item in delay_faults: 
    var, fault = item.split('/')
idx = Inputs.index('N63') 
# Rotate the list such that the given element is at the rightmost position 
rotated_Inputs = Inputs[idx + 1:] + Inputs[:idx + 1]

initial_inputs = {inp: None for inp in rotated_Inputs} 
circuit.set_inputs(**initial_inputs)

# Find test pattern
for fault in stuck_at_faults:
    test_pattern = podem.find_test_pattern(fault)

print(f"Test pattern for fault {fault}: {test_pattern}")