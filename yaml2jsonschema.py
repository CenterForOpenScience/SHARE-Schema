import json
import jsonschema
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def yaml_to_json_schema(yml, title="schema", indent=2, **kwargs):
    outer = dict(
        title=title, type="object", properties=yaml.load(yml, Loader=Loader)
    )
    return json.dumps(outer, indent=indent, **kwargs)

with open('schema-jsonschema.json', 'w') as json_file:
    with open('share.yaml', 'r') as f:
        json_file.write(yaml_to_json_schema(f.read()))

# jsonschema.validate()