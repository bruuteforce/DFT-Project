from circuit_gate_classes import create_test_ckt 
from circuit_gate_classes import generate_test_patterns
from circuit_gate_classes import convert_fault_list
from circuit_gate_classes import check_fault_loc_value
from circuit_gate_classes import Gate
from sync_basics import parse_verilog
from sync_basics import read_verilog_file
import threading
mutex=threading.Lock()

Found_v1=0
Found_v2=0

Out_File="Results_ATPG.txt"

class PODEM:
    def __init__(self, circuit, idx):
        self.circuit = circuit
        self.idx=idx
        self.found_v1=0
        self.v1={}
        self.found_v2=0
        self.v2={}

    def find_test_pattern(self, fault):
        self.circuit.clear_faults()
        self.circuit.inject_fault(fault[0], fault[1])
        
        inputs = list(self.circuit.values.keys())
        return self.recursive_podem(inputs, fault)
    
    def recursive_podem(self, inputs, fault):
        global Found_v2, Found_v1
        if Found_v2==1 and Found_v1==1:
            return None
        if self.check_fault_propagation(fault):
            if Found_v1:
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
        global Found_v1
        self.circuit.inject_fault(fault[0], fault[1])
        self.circuit.evaluate()

        fault_outputs = self.circuit.get_outputs()
        
        self.circuit.clear_faults()
        self.circuit.evaluate()

        no_fault_outputs = self.circuit.get_outputs()
        if (self.found_v1 == 0) and check_fault_loc_value(self.circuit,fault,self.idx):
            self.v1=dict(self.circuit.values)
            self.found_v1=1
            Found_v1=1

        for output in self.circuit.outputs: 
            if fault_outputs[output] is None or no_fault_outputs[output] is None: 
                return False 
            # Check if any output is different 
            if fault_outputs[output] != no_fault_outputs[output]: 
                self.found_v2=1
                self.v2=dict(self.circuit.values)
                return True
        return False

def launcher(podem,Inputs,stuck_at_fault,idx,thr_list):

    rotated_Inputs = Inputs[idx + 1:] + Inputs[:idx + 1]

    initial_inputs = {inp: None for inp in rotated_Inputs} 
    podem.circuit.set_inputs(**initial_inputs)
    #######  mind your changes these are globals
    global Found_v1, Found_v2
    
    # Find test pattern
    test_pattern = podem.find_test_pattern(stuck_at_fault)
    with mutex:
        if(podem.v1):
            list=[]
            for input in Inputs:
                list.append('x' if podem.v1[input] is None else podem.v1[input])
            print(f"V1:{list}")
            
            with open(Out_File, 'a') as f:
                f.write(f"V1:{list}\n")
            input_v1 = podem.v1
            podem.circuit.set_inputs(**input_v1)
            podem.circuit.evaluate()
            list=[]
            for output in Outputs:
                list.append('x' if podem.v1[output] is None else podem.v1[output])
            print(f"output:{list}")
            with open(Out_File, 'a') as f:
                f.write(f"output:{list}\n")
        if(test_pattern):
            list=[]
            for input in Inputs:
                list.append('x' if test_pattern[input] is None else test_pattern[input])
            print(f"V2:{list}")
            with open(Out_File, 'a') as f:
                f.write(f"V2:{list}\n")
            input_v2 = test_pattern
            podem.circuit.set_inputs(**input_v2)
            podem.circuit.evaluate()
            v2_outputs=podem.circuit.get_outputs()
            list=[]
            for output in Outputs:
                list.append('x' if v2_outputs[output] is None else v2_outputs[output])
            print(f"output:{list}")
            with open(Out_File, 'a') as f:
                f.write(f"output:{list}\n")
        
        Found_v2=1

if __name__ == "__main__":

    # Define the circuit and faults
    v_file='c432.v'
    delay_faults = ["N250/STR","N122/STF"]
    
    # v_file='c17.v'
    # delay_faults = ["N11/STF"]
    
    # v_file='test_ckt.v'
    # delay_faults = ["p/STF"]
    
    verilog_content = read_verilog_file(v_file)
    ckt_name, Inputs, Outputs, Wires, Mod_ports = parse_verilog(verilog_content)

    stuck_at_faults = convert_fault_list(delay_faults)

    for index,fault in enumerate(stuck_at_faults):
        threads=[]
        Found_v1=Found_v2=0
        print(f"\nTest Vectors for {delay_faults[index]}:")
        with open(Out_File, 'a') as f:
            f.write(f"\nTest Vectors for {delay_faults[index]}:\n")
        for i in range(len(Inputs)):
            circuit = create_test_ckt(v_file,Inputs,Outputs)
            # Initialize PODEM
            podem = PODEM(circuit,i)
            threads.append(threading.Thread(target=launcher, args=(podem,Inputs,fault,i,threads)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()