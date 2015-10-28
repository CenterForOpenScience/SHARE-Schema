import json
from collections import OrderedDict

import yaml
import argparse

import jsonschema


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    ''' This prevents the order of the schema from becoming muddled when turned into a python dictionary '''
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping
    )

    return yaml.load(stream, OrderedLoader)


def main():
    args = parse_args()
    schema = get_json_schema(args.yaml_path)

    if args.dest:
        write_to_json(schema, args.dest)
    if args.validate:
        if validate(schema, args.test):
            print("{}.yaml validated against {}.json".format(args.yaml_path, args.test))


def parse_args():
    parser = argparse.ArgumentParser(
        description="A command line interface for schema things"
    )

    parser.add_argument('--test', dest='test', type=str, help='The path to a test file to validate against', default='tests/valid.json')
    parser.add_argument('--yaml', dest='yaml_path', type=str, help='The name of the yaml schema file', default='share')
    parser.add_argument('-d', '--dest', dest='dest', type=str, help='The name of the desired json output file', default='schema')
    parser.add_argument('-v', '--validate', dest='validate', help='A flag to validate the schema against a test file', action='store_true')

    return parser.parse_args()


def get_json_schema(yaml_path):
    with open(yaml_path + '.yaml', 'r') as f:
        return ordered_load(f.read())


def validate(schema, path):
    with open(path, 'r') as f:
        test = json.load(f)

    format_checker = jsonschema.FormatChecker(formats=jsonschema.FormatChecker.checkers.keys())
    return jsonschema.validate(test, schema, format_checker=format_checker) is None


def write_to_json(schema, path):
    with open(path + '.json', 'w') as f:
        f.write(json.dumps(schema, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
