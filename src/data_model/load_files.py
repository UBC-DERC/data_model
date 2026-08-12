import pathlib as pt

import yaml


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
        for i in filePath.glob('*.y*ml'):
            output.append(load_file(i))
    else:
        raise FileNotFoundError(f"{filename} is neither a file or directory in the current working directory.")
    return output


def resolve_ref(obj:dict)->dict:
    """_Merge a ``ref:`` target file into ``obj``; return ``obj`` unchanged if none._

    The referenced file is loaded first and the object's own keys are layered
    on top (``loaded | obj``), so a locally-specified key (e.g. a ``comment``)
    overrides the shared reference.

    Args:
        obj (dict): _A YAML object that may contain a ``ref`` key._

    Returns:
        dict: _The object with any ``ref`` target merged in._
    """
    if "ref" in obj:
        return load_file(obj["ref"]) | obj
    return obj
