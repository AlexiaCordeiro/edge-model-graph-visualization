import re


def generate_files(block: list, connected_blocks: list, metadata: dict, function_name: str):
    """
    Generates both files with and without metadata
    """
    file_name = f"generated_files/{function_name}_addapted.cfg"
    final_block = connect_blocks(block, connected_blocks)
    _create_files(final_block, [], file_name)
    if metadata:
        file_name = f"generated_files/{function_name}_metadados.cfg"
        new_block = add_metadata_in_cfg(block, metadata)
        final_block = connect_blocks(new_block, connected_blocks)
        _create_files(final_block, [], file_name)


def connect_blocks(block: list, connected_blocks: list) -> list:
    """
    Connects the main block with the connected block.
    Returns the main block with connected blocks appended.
    """
    if not connected_blocks:
        return block
    
    final_block = block + connected_blocks
    return final_block


def _create_files(block: list, connected_blocks: list, file_name: str):
    """
    Create a new CFG file with the desired block
    """
    try:
        with open(file_name, "w", encoding="utf8") as b:
            for line in block:
                b.write(f"{line}\n")
            if connected_blocks:
                for line in connected_blocks:
                    b.write(f"{line}\n")
    except OSError as e:
        print(f"Error creating file:{e}")


def add_metadata_in_cfg(block: list, metadata: dict) -> list:
    """
    Adds dot info into the cfg so that
    is possible add metadata on model explorer
    """
    new_block = []
    commplete_block = block.copy()
    block.pop(0)
    for line, name in zip(block, metadata):
        if line.startswith("[node") and name in line:
            new_block.append(line)
            new_block.append(metadata[name])

    new_block.insert(0, commplete_block[0])

    return new_block
