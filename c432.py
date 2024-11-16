def not_(input):
    return int(not(input))

def evaluate_c432(inputs,Fault_line):
    # Extract inputs
    N1, N4, N8, N11, N14, N17, N21, N24, N27, N30, \
    N34, N37, N40, N43, N47, N50, N53, N56, N60, N63, \
    N66, N69, N73, N76, N79, N82, N86, N89, N92, N95, \
    N99, N102, N105, N108, N112, N115 = inputs

    # Intermediate signals
    N118 = not_ (N1)
    N119 = not_ (N4)
    N122 = not_ (N11)
    N123 = not_ (N17)
    N126 = not_ (N24)
    N127 = not_ (N30)
    N130 = not_ (N37)
    N131 = not_ (N43)
    N134 = not_ (N50)
    N135 = not_ (N56)
    N138 = not_ (N63)
    N139 = not_ (N69)
    N142 = not_ (N76)
    N143 = not_ (N82)
    N146 = not_ (N89)
    N147 = not_ (N95)
    N150 = not_ (N102)
    N151 = not_ (N108)

    # Logic gates
    N154 = N118 and N4
    N157 = not_ (N8 or N119)
    N158 = not_ (N14 or N119)
    N159 = N122 and N17
    N162 = N126 and N30
    N165 = N130 and N43
    N168 = N134 and N56
    N171 = N138 and N69
    N174 = N142 and N82
    N177 = N146 and N95
    N180 = N150 and N108

    N183 = not_ (N21 or N123)
    N184 = not_ (N27 or N123)
    N185 = not_ (N34 or N127)
    N186 = not_ (N40 or N127)
    N187 = not_ (N47 or N131)
    N188 = not_ (N53 or N131)
    N189 = not_ (N60 or N135)
    N190 = not_ (N66 or N135)
    N191 = not_ (N73 or N139)
    N192 = not_ (N79 or N139)
    N193 = not_ (N86 or N143)
    N194 = not_ (N92 or N143)
    N195 = not_ (N99 or N147)
    N196 = not_ (N105 or N147)
    N197 = not_ (N112 or N151)
    N198 = not_ (N115 or N151)

    N199 = N154 and N159 and N162 and N165 and N168 and N171 and N174 and N177 and N180
    N203 = not_ (N199)
    N213 = not_ (N199)
    N223 = not_ (N199)

    # Outputs
    N329 = not_ (N199)
    N370 = not_ (N154 and N159 and N162 and N165 and N168 and N171 and N174 and N177 and N180)

    N421 = not_ (not_ (N154 and N159 and N162 and N165 and N168 and N171 and N174 and N177 and N180) or N199)
    N430 = not_ (N421)
    N431 = N430
    N432 = not_ (N421 and N430)

    # Return outputs
    return locals()[Fault_line], N223, N329, N370, N421, N430, N431, N432