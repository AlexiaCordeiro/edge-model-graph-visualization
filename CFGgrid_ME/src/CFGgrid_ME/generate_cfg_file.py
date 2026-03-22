import re

from .get_nodes import check_if_layer_called, get_correct_block_via_layer


def generate_files(model: list, block: list, metadata: dict, function_name: str):
    """
    Generates both files with and without metadata
    """
    connected_blocks = collect_all_connected_blocks(model, block)
    file_name = f"generated_files/{function_name}_addapted.cfg"
    final_block = connect_blocks(block, connected_blocks)
    _create_files(final_block, file_name)
    if metadata:
        file_name = f"generated_files/{function_name}_metadados.cfg"
        new_block = add_metadata_in_cfg(block, metadata)
        final_block = connect_blocks(new_block, connected_blocks)
        _create_files(final_block, file_name)


def collect_all_connected_blocks(model: list, block: list) -> list:
    """
    Recursively collects all blocks connected to the given block.
    """
    visited = set()
    collected_blocks = []

    def _collect_recursive(current_block):
        layer_connections = check_if_layer_called(current_block)
        for op, connected_layer in layer_connections.items():
            layer_addr = connected_layer.replace('[', '').replace(']', '').split(':')[0]
            if layer_addr not in visited:
                visited.add(layer_addr)
                connected_block = get_correct_block_via_layer(model, {op: connected_layer})
                if connected_block and connected_block not in collected_blocks:
                    collected_blocks.append(connected_block)
                    _collect_recursive(connected_block)

    _collect_recursive(block)
    all_connected = [line for block in collected_blocks for line in block]
    return all_connected


def connect_blocks(block: list, connected_blocks: list) -> list:
    """
    Connects the main block with the connected block.
    Returns the main block with connected blocks appended.
    """
    if not connected_blocks:
        return block
    
    final_block = block + connected_blocks
    return final_block


def _create_files(block: list, file_name: str):
    """
    Create a new CFG file with the desired block
    """
    try:
        with open(file_name, "w", encoding="utf8") as b:
            for line in block:
                b.write(f"{line}\n")
    except OSError as e:
        print(f"Error creating file:{e}")


def add_metadata_in_cfg(block: list, metadata: dict) -> list:
    """
    Adds dot info into the cfg so that
    is possible add metadata on model explorer
    """
    new_block = []
    complete_block = block.copy()
    cfg_header = complete_block.pop(0)
    new_block.append(cfg_header)
    
    for line in complete_block:
        if line.startswith("[node"):
            op_name = line.split()[2]
            if op_name in metadata:
                new_block.append(line)
                new_block.append(metadata[op_name])
            else:
                new_block.append(line)
        else:
            new_block.append(line)
    
    return new_block

    commplete_block = block.copy()
    block.pop(0)
    for line, name in zip(block, metadata):
        if line.startswith("[node") and name in line:
            new_block.append(line)
            new_block.append(metadata[name])

    new_block.insert(0, commplete_block[0])
    return new_block
