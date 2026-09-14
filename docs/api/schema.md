# JSON Schema

The data model YAML format is formally defined by a JSON Schema, auto-generated
from the Pydantic models in [`object_classes.py`](object_classes.md).

## Download

**[Download schema.json](../schema.json)**

## Usage

### Editor autocompletion (VS Code)

Add this to the top of your YAML files to enable validation and autocompletion:

```yaml
# yaml-language-server: $schema=https://ubc-derc.github.io/data_model/schema.json
```

Or configure VS Code's `settings.json`:

```json
{
  "yaml.schemas": {
    "https://ubc-derc.github.io/data_model/schema.json": ["**/data_definitions/**/*.yaml"]
  }
}
```

### Programmatic validation

You can validate YAML files against the schema using any JSON Schema validator:

```python
import json
import yaml
from jsonschema import validate

with open("schema.json") as f:
    schema = json.load(f)

with open("my_database.yaml") as f:
    data = yaml.safe_load(f)

validate(instance=data, schema=schema)
```

## Schema structure

The schema defines these primary objects:

| Object | Description |
|--------|-------------|
| `DDL_Dict` | Root database definition |
| `schema_dict` | A database schema containing tables |
| `table_dict` | A table with columns, constraints, and indexes |
| `column_dict` | A column definition |
| `constraint_dict` | A table constraint (PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE) |
| `index_dict` | A table index |
| `reference_dict` | Foreign key target reference |

See the [Object Classes](object_classes.md) documentation for detailed field descriptions.
