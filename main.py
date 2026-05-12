
def main():
    import data_model as dm
    from yaml import safe_load
    
    schema = safe_load("validation.yaml")
    cows = dm.load_files("data_definitions/tables/cows.yaml")
    dm.validate(schema, cows)
    

if __name__ == "__main__":
    main()
