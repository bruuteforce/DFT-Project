from itertools import product

class Gate:
    def __init__(self, name, operation, inputs, output):
        self.name = name
        self.operation = operation
        self.inputs = inputs
        self.output = output

    def evaluate(self, values, faults):
        # Apply the fault if it affects this gate's output
        if self.output in faults:
            fault_type = faults[self.output]
            if fault_type == 'SA0':
                values[self.output] = 0
            elif fault_type == 'SA1':
                values[self.output] = 1
            return
        
        inputs = [values[inp] for inp in self.inputs]
        if self.operation == 'OR':
            self.output_value = inputs[0] | inputs[1]
        elif self.operation == 'AND':
            self.output_value = inputs[0] & inputs[1]
        elif self.operation == 'XOR':
            self.output_value = inputs[0] ^ inputs[1]
        elif self.operation == 'NOR':
            self.output_value = int(not (inputs[0] | inputs[1]))
        elif self.operation == 'NOR3':
            self.output_value = int(not (inputs[0] | inputs[1] | inputs[2]))
        elif self.operation == 'XOR3':
            self.output_value = inputs[0] ^ inputs[1] ^ inputs[2]
        else:
            raise ValueError('Unknown operation')
        
        values[self.output] = self.output_value


class Circuit:
    def __init__(self):
        self.gates = []
        self.inputs = []
        self.outputs = []
        self.values = {}
        self.faults = {}

    def add_gate(self, gate):
        self.gates.append(gate)

    def set_inputs(self, **kwargs):
        for inp, value in kwargs.items():
            self.values[inp] = value

    def inject_fault(self, fault_type, fault_location):
        self.faults[fault_location] = fault_type

    def clear_faults(self):
        self.faults = {}

    def evaluate(self):
        for gate in self.gates:
            gate.evaluate(self.values, self.faults)
        # print(self.values)

    def get_output(self, output):
        return self.values[output]


# Define the circuit
def create_test_ckt():
    circuit = Circuit()
    
    # Define gates as (name, operation, [inputs], output)
    circuit.add_gate(Gate('G1', 'OR', ['C', 'D'], 'g'))
    circuit.add_gate(Gate('G2', 'AND', ['C', 'g'], 'h'))
    circuit.add_gate(Gate('G3', 'AND', ['g', 'D'], 'k'))
    circuit.add_gate(Gate('G4', 'OR', ['h', 'k'], 'm'))
    circuit.add_gate(Gate('G5', 'XOR', ['E', 'F'], 'l'))
    circuit.add_gate(Gate('G6', 'NOR3', ['A', 'B', 'm'], 'p'))
    circuit.add_gate(Gate('G7', 'OR', ['m', 'B'], 'q'))
    circuit.add_gate(Gate('G8', 'OR', ['B', 'l'], 's'))
    circuit.add_gate(Gate('G9', 'AND', ['A', 'p'], 'r'))
    circuit.add_gate(Gate('G10', 'AND', ['A', 'm'], 'u'))
    circuit.add_gate(Gate('G11', 'AND', ['q', 's'], 'w'))
    circuit.add_gate(Gate('G12', 'XOR3', ['r', 'u', 'w'], 'Z'))
    
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
    
def generate_test_patterns(circuit, faults):
    test_patterns1 = []
    test_patterns2 = []
    inputs = ['A', 'B', 'C', 'D', 'E', 'F']
    input_combinations = list(product([0, 1], repeat=len(inputs)))
    
    for fault in faults:
        found_v1=0
        for input_combination in input_combinations:
            circuit.set_inputs(**dict(zip(inputs, input_combination)))
            inject_fault(circuit, fault)
            circuit.evaluate()
            fault_output = circuit.get_output('Z')
            circuit.clear_faults()
            circuit.evaluate()
            no_fault_output = circuit.get_output('Z')
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
circuit = create_test_ckt()

#delay faults
delay_faults = ["w/STR","p/STF"]

stuck_at_faults = convert_fault_list(delay_faults)

# Generate test patterns
test_patterns1, test_patterns2 = generate_test_patterns(circuit, stuck_at_faults)


for p1,p2 in zip(test_patterns1,test_patterns2):
    print(f"Test pattern 1:  {p1}")
    print(f"Test pattern 2: for {p2[1]}: {p2[0]}")