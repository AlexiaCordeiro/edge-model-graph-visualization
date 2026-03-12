def generate_files(block: list, metadata: dict, function_name: str):
    """
    Generates both files with and without metadata
    """
    file_name = f"generated_files/{function_name}_addapted.cfg"
    _create_files(block, file_name)
    if metadata:
        file_name = f"generated_files/{function_name}_metadados.cfg"
        new_block = add_metadata_in_cfg(block, metadata)
        _create_files(new_block, file_name)


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
    commplete_block = block.copy()
    block.pop(0)
    for line, name in zip(block, metadata):
        if line.startswith("[node") and name in line:
            new_block.append(line)
            new_block.append(metadata[name])

    new_block.insert(0, commplete_block[0])

    return new_block
