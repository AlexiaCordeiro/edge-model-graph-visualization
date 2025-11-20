"""
subprocess: used to run terminal commands via python
"""

import subprocess


def get_model(model_path: str) -> list:
    """
    Get the model file path and returns a list where every line
    in the file is a list inside the model list
    """
    model = []
    try:
        with open(model_path, "r", encoding="utf8") as m:
            model = [line.strip() for line in m if line.strip()]
    except OSError as e:
        print(f"Error reading file: {e}")

    return model


def get_correct_block(model: list, function_name: str) -> list:
    """
    Based on the list with the lines of the CFG in model,
    this funcction gets the specific block informed by the user
    via function_name
    """

    block = []
    init_block = -1
    finish_block = -1

    for i, line in enumerate(model):
        if line.startswith("[cfg") and function_name in line:
            init_block = i
            break

    for i in range(init_block + 1, len(model)):
        if model[i].startswith("[cfg"):
            break

        finish_block = i

    block = model[init_block : finish_block + 1]

    return block


def _create_cfg_desired(block: list, function_name: str):
    """
    Create a new CFG file with the desired block
    """
    try:
        with open(f"{function_name}_addapted.cfg", "a", encoding="utf8") as b:
            for line in block:
                b.write(f"{line}\n")
    except OSError as e:
        print(f"Error creating file:{e}")


def _run_model(file_path: str):
    """
    Runs a terminal command to start model explorer via python
    """
    model_run = f"model-explorer {file_path} --host=0.0.0.0 --extensions CFGgrid_ME"
    subprocess.run(model_run, shell=True, check=True)


def get_metadata(json_path: str) -> list:
    """
    Will get the metadata via the json file informed
    """
    json_data = []
    try:
        with open(json_path, "r", encoding="utf8") as j:
            json_data = [line.strip() for line in j if line.strip()]
    except OSError as e:
        print(f"Error getting json file: {e}")

    return json_data


def _treat_metadata(json_data: list):
    print("json_data")


def main():
    """Get values"""
    model_path = input("CFG PATH: ")
    json_path = input("JSON PATH: ")
    function_name = input("FUNCTION NAME: ").lower()

    model = get_model(model_path)
    block = get_correct_block(model, function_name)
    _create_cfg_desired(block, function_name)
    file_path = f"{function_name}_addapted.cfg"
    json_data = get_metadata(json_path)
    _treat_metadata(json_data)
    _run_model(file_path)


if __name__ == "__main__":
    main()
