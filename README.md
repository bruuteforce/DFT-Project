ATPG for Delay Faults:

Usage:
run the sync++.py python script by giving the proper verilog netlist file name of a ciruit and the fault list to generate the test patterns for, in the same script.

Section in the script where netlist filename and fault list can be given:
if __name__ == "__main__":

    # Define the circuit and faults
    v_file='c432.v'
    delay_faults = ["N250/STR","N122/STF"]
    
    # v_file='c17.v'
    # delay_faults = ["N11/STF"]
    
    # v_file='test_ckt.v'
    # delay_faults = ["p/STF"]

[test_ckt.v : this is the sample circuit given]

fault format: "<fault_location>/<STR or STF>"
Make sure the <fault_location> is an existing line name in the circuit

