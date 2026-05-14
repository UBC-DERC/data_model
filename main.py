
def main():
    import data_model as dm
    import pathlib as pt
    from yaml import safe_load
    
    with open(pt.Path("validation.yaml"), 'r') as schemaFile:
        validation = safe_load(schemaFile)
    cows = dm.load_database("data_definitions/dairymodel.yaml", validation = validation)
    print(cows)
if __name__ == "__main__":
    main()
