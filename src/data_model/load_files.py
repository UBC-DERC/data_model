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
    output = []
    if filePath.is_file():
        with open(filePath, "r") as file:
            output = yaml.safe_load(file)
            if isinstance(output, list):
                output = output[0]
    elif filePath.is_dir():
        output = []
        for i in filePath.glob('*.y*ml'):
            output.append(load_file(i))
    else:
        raise FileNotFoundError(f"{filename} is neither a file or directory in the current working directory.")
    return output


def resolve_ref(obj:dict, base_dir:str|Path=".")->dict:
    """_Merge a ``ref:`` target file into ``obj``; return ``obj`` unchanged if none._

    The referenced file is loaded first and the object's own keys are layered
    on top (``loaded | obj``), so a locally-specified key (e.g. a ``comment``)
    overrides the shared reference.

    The ``ref`` path is resolved relative to ``base_dir`` (the directory of the
    file that contains the ref). Absolute refs are used as-is, since joining an
    absolute path onto ``base_dir`` yields the absolute path.

    Args:
        obj (dict): _A YAML object that may contain a ``ref`` key._
        base_dir (str | Path): _Directory the ``ref`` is resolved against._

    Returns:
        dict: _The object with any ``ref`` target merged in._
    """
    if "ref" in obj:
        return load_file(Path(base_dir) / obj["ref"]) | obj
    return obj


def base_dir_of(filename:str|Path)->Path:
    """_Return the directory that refs inside ``filename`` resolve against._

    For a file this is its parent directory; for a directory (loaded via
    globbing) it is the directory itself, because the globbed files live
    directly inside it and carry refs relative to that location.
    """
    p = Path(filename)
    return p if p.is_dir() else p.parent
