def sample_circuit(inputs, Fault_line):
    A, B, C, D, E, F = inputs
    # Simulate the circuit
    g = C or D
    h = C and g
    k = g and D
    m = h or k 
    l = E ^ F
    p = int(not (A or B or m))
    q = m or B
    s = B or l
    r = A and p
    u = A and m
    w = q and s
    Z = r ^ u ^ w
    return locals()[Fault_line], Z