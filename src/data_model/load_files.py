import yaml
from pathlib import Path

def load_file(filename:str)->dict:
    """_load YAML file into a dict for internal use._

    Args:
        filename (str): _A valid filename or directory._

    Returns:
        dict: _A dict model _
    """
    filePath = Path(filename)
    if filePath.is_file():
        with open(filePath, "r") as file:
            try:
                output = yaml.safe_load(file)[0]
            except KeyError:
                print(f'The object loaded from {filePath} does not have a key [0]:')
                print(yaml.safe_load(file))
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

def load_yaml_with_refs(path: Path):
    data = yaml.safe_load(path.read_text())
    return _resolve(data, base_dir=path.parent)

def _resolve(node, base_dir: Path):
    if isinstance(node, dict):
        if "ref" in node:
            ref_path = (base_dir / node["ref"]).resolve()
            # nested refs resolve relative to *this* file's dir:
            return load_yaml_with_refs(ref_path)
        return {k: _resolve(v, base_dir) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve(item, base_dir) for item in node]
    return node