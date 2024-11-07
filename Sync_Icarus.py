import pandas as pd
import os

Out_File="Results_ATPG.txt"
with open(Out_File, 'w') as f:
    pass

truth_table=None
def parse_file(filename="C:\iverilog\TT.csv"):
    global truth_table
    truth_table = pd.read_csv(filename)
    #print(truth_table)

def worker(tt=truth_table,fault="A/STF",outputs=["Z"],inputs=["A","B","C","D","E","F"]):
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

    num_rows = tt.shape[0]
    pairs=[]
    for output in outputs:
        for i in range(num_rows): 
            for j in range(i + 1, num_rows): 
                if tt.iloc[i][wire] == V1_wire and tt.iloc[j][wire] == V2_wire and tt.iloc[i][output] != tt.iloc[j][output]: 
                    diff = tt.loc[i, inputs] != tt.loc[j, inputs]  
                    sum = 0
                    for d in diff:
                        sum+=d
                    if(sum == 1):
                        pairs.append((i,j))
    with open(Out_File, 'a') as f:
        print("Test Vectors for fault:",fault)
        f.write(f"Test Vectors for fault:{fault}\n")
    if not pairs:
        with open(Out_File, 'a') as f:
            print(f"Fault Not Detected.")
            f.write(f"\tFault Not Detected.\n")
    else:
        for pair in pairs:
            with open(Out_File, 'a') as f:
                row_str = ' '.join([f"{col}" for col, val in tt.iloc[pair[0]].items()]) 
                print(f"[{row_str}]")
                f.write(f"\t[{row_str}]\n")
                row_str = ' '.join([f"{val}" for col, val in tt.iloc[pair[0]].items()]) 
                print(f"[{row_str}]")
                f.write(f"V1:\t[{row_str}]\n")
                row_str = ' '.join([f"{val}" for col, val in tt.iloc[pair[1]].items()]) 
                print(f"[{row_str}]")
                f.write(f"V2:\t[{row_str}]\n")
            break 

os.system(f"C:\iverilog\\bin\iverilog.exe -I E:\DFT\project\ -o TB E:\DFT\project\\testbench.v")   
os.system(f"C:\iverilog\\bin\\vvp.exe -l TT.csv TB")  
parse_file(f"E:\DFT\project\TT.csv")

####################################################
Fault_List=["B/STR","w/STF","p/STF","A/STR"]
Inputs=["A","B","C","D","E","F"]
Outputs=["Z"]
for fault in Fault_List:
    worker(truth_table,fault,Outputs,Inputs)