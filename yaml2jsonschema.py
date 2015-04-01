import json
import jsonschema
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    schema = get_yaml_schema('share.yaml')
    write_to_json(schema, 'schema.json')

    validate(schema, 'test.json')

def validate(schema, path):
    with open(path, 'r') as f:
        test = json.load(f)

    format_checker = jsonschema.FormatChecker(formats=jsonschema.FormatChecker.checkers.keys())
    return jsonschema.validate(test, schema, format_checker=format_checker)

def write_to_json(schema, path):
    with open(path, 'w') as f:
        f.write(json.dumps(schema, indent=4))

def get_yaml_schema(path):
    with open(path, 'r') as f:
        return yaml.load(f.read(), Loader=Loader)

if __name__ == '__main__':
    main()
