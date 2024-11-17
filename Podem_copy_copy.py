from D_alg_copy_copy import create_test_ckt 
from D_alg_copy_copy import generate_test_patterns
from D_alg_copy_copy import convert_fault_list
from D_alg_copy_copy import check_fault_loc_value
from D_alg_copy_copy import Gate
from Sync_Icarus_extended import parse_verilog
from Sync_Icarus_extended import read_verilog_file
import threading

Found_v1=0
Found_v2=0

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
        # self.circuit.print_inputs(f"{self.idx}::check:input:faulty:")
        # self.circuit.print_outputs(f"{self.idx}::check:output:faulty")
        fault_outputs = self.circuit.get_outputs()
        
        self.circuit.clear_faults()
        self.circuit.evaluate()
        # self.circuit.print_inputs(f"{self.idx}::check:input:fault_free:")
        # self.circuit.print_outputs(f"{self.idx}::check:output:fault_free:")
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
    # print(f"{idx}::launcher[{idx}]")
    # Rotate the list such that the given element is at the rightmost position 
    rotated_Inputs = Inputs[idx + 1:] + Inputs[:idx + 1]

    initial_inputs = {inp: None for inp in rotated_Inputs} 
    podem.circuit.set_inputs(**initial_inputs)
    #######  mind your changes these are globals
    global Found_v1, Found_v2
    
    # Find test pattern
    test_pattern = podem.find_test_pattern(stuck_at_fault)

    if(podem.v1):
        # print(f"{idx}:: Test pattern V1: {podem.v1}")
        list=[]
        for input in Inputs:
            list.append(podem.v1[input])
        print(f"V1:{list}")
    if(test_pattern):
        # print(f"{idx}:: Test pattern for fault {fault}: {test_pattern}")
        list=[]
        # list1=[]
        for input in Inputs:
            list.append(test_pattern[input])
            # list1.append(podem.v2[input])
        print(f"V2:{list}")
        # print(f"V2_dash:{list1}")
    
    Found_v2=1

if __name__ == "__main__":

    # Define the circuit
    v_file='c432.v'
    delay_faults = ["N250/STR","N177/STF"]
    
    # v_file='c17.v'
    # delay_faults = ["N11/STF"]
    
    # v_file='test_ckt.v'
    # delay_faults = ["p/STF"]
    
    verilog_content = read_verilog_file(v_file)
    ckt_name, Inputs, Outputs, Wires, Mod_ports = parse_verilog(verilog_content)

    stuck_at_faults = convert_fault_list(delay_faults)

    # Generate test patterns
    #test_patterns1, test_patterns2 = generate_test_patterns(circuit, stuck_at_faults,Inputs,Outputs)


    #for p1,p2 in zip(test_patterns1,test_patterns2):
    #    print(f"Test pattern 1:  {p1}")
    #    print(f"Test pattern 2: for {p2[1]}: {p2[0]}")
    for index,fault in enumerate(stuck_at_faults):
        threads=[]
        Found_v1=Found_v2=0
        print(f"\nTest Vectors for {delay_faults[index]}:")
        for i in range(len(Inputs)):
            circuit = create_test_ckt(v_file,Inputs,Outputs)
            # Initialize PODEM
            podem = PODEM(circuit,i)
            threads.append(threading.Thread(target=launcher, args=(podem,Inputs,fault,i,threads)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()