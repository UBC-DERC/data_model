from pathlib import Path

def document_database(database:dict, path:Path)->None:
    docs = Path('docs/')
    database_page(database, docs / 'database')
    
def database_page(database:dict, path:Path)->None:
    if not path.is_dir():
        path.mkdir()
    fileOutput = []
    fileOutput.append(f"# {database['name']}")
    fileOutput.append(f"Description:\n**{database.get('comment', "No comment present")}**")
    fileOutput.append("\n## Schemas")
    for i in database.get('schema'):
        fileOutput.append(f"* [{i.get('name')}](./{i.get('name')}/{i.get('name')}.md)")
        schema_page(i, path / f'{i.get('name')}')
    with open(path / 'index.md', 'w') as fileOut:
        for line in fileOutput:
            fileOut.write("".join(line) + '\n')
    

def schema_page(schema: dict, path:Path):
    if not path.is_dir():
        path.mkdir()
    fileOutput = []
    fileOutput.append(f"# {schema.get('name')}")
    fileOutput.append(f"Description:\n**{schema.get('comment', "No comment present")}**")
    fileOutput.append("\n## Tables\n")
    for i in schema.get('tables'):
        if type(i) is list:
            fileOutput.append("This schema contains no tables.")
        else:
            fileOutput.append(f"* [{i.get('name')}](tables/{i.get('name')}.md)")
            table_page(i, path / 'tables')
    with open(path / f"{schema.get('name')}.md", 'w') as fileOut:
        for line in fileOutput:
            fileOut.write("".join(line) + '\n')

def table_page(table: dict, path:Path):
    if not path.is_dir():
        path.mkdir()
    fileOutput = []
    fileOutput.append(f"# {table.get('name')}")
    fileOutput.append(f"Description:\n**{table.get('comment', "No comment present")}**")
    fileOutput.append("\n## Columns\n")
    fileOutput.append(columnPrint(table.get('columns')))
    fileOutput.append("\n## Constraints\n")
    fileOutput.append(constraintPrint(table.get('constraints', [])))
    fileOutput.append("\n## Indexes\n")
    fileOutput.append("\n## Relationships\n")
    with open(path / f"{table.get('name')}.md", 'w') as fileOut:
        for line in fileOutput:
            fileOut.write("".join(line) + '\n')
    
def columnFormatter(columns):
    keys = set()
    for i in columns:
        keys.update(i.keys())
    for i in range(len(columns)):
        columns[i] = {j: columns[i].get(j) for j in keys}
    return(columns)

def columnPrint(columns:dict) -> list:
    from py_markdown_table.markdown_table import markdown_table

    keys = ['name', 'type', 'comment']
    columnPrint = []
    for i in columns:
        columnPrint.append({k: i.get(k) for k in keys})
    try:
        return markdown_table(columnFormatter(columnPrint)).set_params(row_sep = 'markdown', quote=False).get_markdown()
    except:
        print("This table is broken")

def constraintPrint(constraints:dict)->list:
    from py_markdown_table.markdown_table import markdown_table
    if len(constraints) == 0:
        return "This table has no constraints"
    keys = ['name', 'type', 'def', 'comment']
    constraintPrint = []
    for i in constraints:
        constraintPrint.append({k: i.get(k) for k in keys})
    try:
        return markdown_table(constraintPrint).set_params(row_sep = 'markdown', quote=False).get_markdown()
    except:
        print(constraints)