import yaml
import pathlib as pt

def load_file(filename:str)->dict:
    """_load YAML file into a dict for internal use._

    Args:
        filename (str): _A valid filename or directory._

    Returns:
        dict: _A dict model _
    """
    filePath = pt.Path(filename)
    if filePath.is_file():
        with open(filePath, "r") as file:
            output = yaml.safe_load(file)[0]
    elif filePath.is_dir():
        output = []
        for i in filePath.glob('*.yaml'):
            output.append(load_file(i))
    else:
        raise FileNotFoundError(f"{filename} is neither a file or directory in the current working directory.")
    return output
