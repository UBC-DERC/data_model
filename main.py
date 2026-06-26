
def main():
    import data_model as dm
    import pathlib as pt
    from yaml import safe_load, safe_dump
    
    with open(pt.Path("validation.yaml"), 'r') as schemaFile:
        validation = safe_load(schemaFile)
    cows = dm.load_database("data_definitions/dairymodel.yaml", validation = validation)
    dm.document_database(cows, 'docs')
    with open('output.yaml', 'w') as file:
        safe_dump(cows.model_dump(), file)

if __name__ == "__main__":
    main()
