import yaml
import pathlib

def load_files(filename)->dict:
    with open(filename, "r") as file:
        output = yaml.safe_load(file)
    print(output)
    return output