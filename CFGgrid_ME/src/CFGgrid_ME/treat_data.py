import re


def treat_metadata(metadata: list, node_addresses: set) -> dict:
    """
    Groups assembly lines into blocks keyed by node start address.
    A new block begins whenever a line's address matches a known node address.
    """
    blocks = {}
    current_block = None
    current_instructions = []

    for line in metadata:
        addr = line.split(":")[0]
        if addr in node_addresses:
            if current_block is not None:
                blocks[current_block] = current_instructions
            current_block = addr
            current_instructions = [line]
        else:
            if current_block is not None:
                current_instructions.append(line)

    if current_block is not None:
        blocks[current_block] = current_instructions

    return blocks

