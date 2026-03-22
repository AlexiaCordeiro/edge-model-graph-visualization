import re


def treat_metadata(metadata: list) -> dict:
    meta_dict = {}
    current_key = None
    current_instructions = []
    for line in metadata:
        line = line.strip()
        if (
            line.startswith("digraph")
            or line.startswith("label")
            or line.startswith("node")
            or line.startswith("Entry")
            or line.startswith("}")
        ):
            continue
        if "label" in line:
            if current_key and current_instructions:
                meta_dict[current_key] = current_instructions
            key_match = re.search(r'"([0-9a-fA-Fx]+)"\s*\[label="\{', line)
            if key_match:
                current_key = key_match.group(1)
                current_instructions = []
            continue
        current_instructions = clean_metadata(line, current_instructions)

    if current_key and current_instructions:
        meta_dict[current_key] = current_instructions
    return meta_dict


def clean_metadata(line: str, current_instructions: list) -> list:
    if "&nbsp;&nbsp;" in line:
        instruction = line.replace("&nbsp;&nbsp;", "").replace(r"\l", "").strip()
        if instruction.endswith("\\"):
            instruction = instruction[:-1].strip()
        if instruction:
            current_instructions.append(instruction)

    return current_instructions
