import re

def parse_gate_line(line):
    # Regex to match the gate line
    pattern = re.compile(r'(\w+)\s+(\w+)_(\d+)\s+\((\w+),\s*([\w, ]+)\);')
    match = pattern.match(line)
    if not match:
        return None
    
    operation, gate, index, output, inputs_str = match.groups()
    inputs = [inp.strip() for inp in inputs_str.split(',')]
    
    return {
        'gate': f'{gate}',
        'gate_name': f'{gate}_{index}',  # Adding the full gate name here
        'output': output,
        'inputs': inputs
    }

# Read lines from a file and parse them
def parse_file(filename):
    gates = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                gate_info = parse_gate_line(line)
                if gate_info:
                    gates.append(gate_info)
    return gates

