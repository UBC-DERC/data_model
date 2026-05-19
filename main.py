
def main():
    import data_model as dm
    import pathlib as pt
    from yaml import safe_load
    from json import dumps
    
    with open(pt.Path("validation.yaml"), 'r') as schemaFile:
        validation = safe_load(schemaFile)
    cows = dm.load_database("data_definitions/dairymodel.yaml", validation = validation)
    dm.document_database(cows, 'docs')
    # print(dumps(cows))

if __name__ == "__main__":
    main()
