from .load_files import load_file, resolve_ref, base_dir_of


def load_columns(filename:str)->dict:
    return resolve_ref(load_file(filename), base_dir_of(filename))
