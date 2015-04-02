import json
import yaml
import argparse
import jsonschema

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    args = parse_args()
    schema = get_json_schema(args.yaml_path)

    if args.dest:
        write_to_json(schema, args.dest)
    if args.docs:
        docs = gen_docs(schema, docs)
    if args.validate:
        validate(schema, args.test)


def parse_args():
    parser = argparse.ArgumentParser(description="A command line interface for schema things")

    parser.add_argument('--test', dest='test', type=str, help='The path to the test json file', default='test')
    parser.add_argument('--yaml', dest='yaml_path', type=str, help='The path to the yaml schema file', default='share')
    parser.add_argument('--dest', dest='dest', type=str, help='The path to the desired output file', default='')
    parser.add_argument('--docs', dest='docs', type=str, help='The path to the desired location for documentation', default='')
    parser.add_argument('--validate', dest='validate', type=bool, help='A flag to validate the schema against a test file', default=False)
    parser.add_argument('--format', dest='format', type=str, help='Specify the format you would like your documentation in', default='csv')

    return parser.parse_args()


def get_json_schema(yaml_path):
    with open(yaml_path + '.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=Loader)


def validate(schema, path):
    with open(path + '.json', 'r') as f:
        test = json.load(f)

    format_checker = jsonschema.FormatChecker(formats=jsonschema.FormatChecker.checkers.keys())
    return jsonschema.validate(test, schema, format_checker=format_checker)


def write_to_json(schema, path):
    with open(path, 'w') as f:
        f.write(json.dumps(schema, indent=4))

def gen_docs(schema, path):
    pass

if __name__ == '__main__':
    main()
