import pandas as pd
import os


truth_table=None
def parse_file(filename="C:\iverilog\TT.csv"):
    global truth_table
    truth_table = pd.read_csv(filename,encoding='utf-16')
    print(truth_table)
    # truth_table = pd.read_csv("C:\\iverilog\\TT1.csv")
    # print(truth_table)
    # truth_table = pd.read_csv("C:\\iverilog\\test.csv")
    # print(truth_table)

def worker(tt=truth_table,fault="B/STR",output="Z",inputs=["A","B","C","D","E","F"]):
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
    for i in range(num_rows): 
        for j in range(i + 1, num_rows): 
            if tt.iloc[i][wire] == V1_wire and tt.iloc[j][wire] == V2_wire and tt.iloc[i][output] != tt.iloc[j][output]: 
                diff = tt.loc[i, inputs] != tt.loc[j, inputs]  
                sum = 0
                for d in diff:
                    sum+=d
                if(sum == 1):
                    pairs.append((i,j))
                #elif(sum > 1):
                    #print("check if this can this be a test vector pair.")
    print(wire,V1_wire,V2_wire,output,num_rows,pairs)   
    print("Test Vectors for fault:%s:",fault)
    for pair in pairs:
        print(tt.iloc[pair[0]].values,tt.iloc[pair[1]].values)
        break 
    
parse_file("C:\\iverilog\\TT.csv")
worker(truth_table)