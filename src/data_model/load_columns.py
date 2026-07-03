from .load_files import load_file, resolve_ref


def load_columns(filename:str)->dict:
    return resolve_ref(load_file(filename))
