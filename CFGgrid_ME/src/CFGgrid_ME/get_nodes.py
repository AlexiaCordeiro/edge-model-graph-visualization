
import re


def get_correct_block_via_func_name(model: list, function_name: str):
    """
    Based on the list with the lines of the CFG in model,
    this function gets the specific block informed by the user
    via function_name
    """

    block = []
    init_block = -1
    finish_block = -1
    correct_start = "::" + function_name
    for i, line in enumerate(model):
        if (line.startswith("[cfg") 
        and function_name in line 
        and correct_start in line):
            init_block = i
            break

    for i in range(init_block + 1, len(model)):
        if model[i].startswith("[cfg"):
            break

        finish_block = i

    block = model[init_block : finish_block + 1]
    return block

def get_correct_block_via_layer(model: list, layer_name: dict):
    """
    Based on the list with the lines of the CFG in model,
    this function gets the specific block informed by the user
    via layer_name
    """
    block = []
    init_block = -1
    finish_block = -1
    layer_name = list(layer_name.values())[0].replace('[', '').replace(']', '')
    for i, line in enumerate(model):
        if (line.startswith("[cfg") 
        and layer_name in line):
            init_block = i
            break

    for i in range(init_block + 1, len(model)):
        if model[i].startswith("[cfg"):
            break

        finish_block = i

    block = model[init_block : finish_block + 1]
    return block

def check_if_layer_called(block: list) -> dict:
    """
    Checks if the block has a call to another layer and returns the name of the layer
    """
    layer_connection = {}
    for line in block:
        if line.startswith("[node"):
            op = parse_node_line(line, 3)
            connected_layer = parse_node_line(line, 6)
            if connected_layer:
                layer_connection[op] = connected_layer
    if layer_connection is not None:
        return layer_connection
    return {}

def parse_node_line(node_line: str, element_index: int) -> str:
    """
    Parses a node line and extracts a specific element by index.
    """
    line = node_line.strip()
    if line.startswith('[') and line.endswith(']'):
        line = line[1:-1].strip()
    
    elements = []
    current = ""
    bracket_depth = 0
    
    for char in line:
        if char == '[':
            bracket_depth += 1
            current += char
        elif char == ']':
            bracket_depth -= 1
            current += char
        elif char == ' ' and bracket_depth == 0:
            if current.strip():
                elements.append(current.strip())
            current = ""
        else:
            current += char
    
    if current.strip():
        elements.append(current.strip())
    
    if 0 <= element_index - 1 < len(elements):
        return elements[element_index - 1]
    return ""
