import csv
import json
import yaml
import argparse

import jsonschema
from jsonpointer import resolve_pointer

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
        gen_docs(schema, args.docs)
    if args.validate:
        if validate(schema, args.test):
            print("{}.yaml validated against {}.json".format(args.yaml_path, args.test))


def parse_args():
    parser = argparse.ArgumentParser(description="A command line interface for schema things")

    parser.add_argument('--test', dest='test', type=str, help='The path to a test file to validate against', default='tests/valid.json')
    parser.add_argument('--yaml', dest='yaml_path', type=str, help='The name of the yaml schema file', default='share')
    parser.add_argument('-d', '--dest', dest='dest', type=str, help='The name of the desired json output file', default='schema')
    parser.add_argument('--docs', dest='docs', type=str, help='The full path (extension included) to the desired location for documentation', default='')
    parser.add_argument('-v', '--validate', dest='validate', help='A flag to validate the schema against a test file', action='store_true')

    return parser.parse_args()


def get_json_schema(yaml_path):
    with open(yaml_path + '.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=Loader)


def validate(schema, path):
    with open(path, 'r') as f:
        test = json.load(f)

    format_checker = jsonschema.FormatChecker(formats=jsonschema.FormatChecker.checkers.keys())
    return jsonschema.validate(test, schema, format_checker=format_checker) is None


def write_to_json(schema, path):
    with open(path + '.json', 'w') as f:
        f.write(json.dumps(schema, indent=4))


def gen_docs(schema, path):
    rows = [('name', 'type', 'format', 'required', 'description')]
    for key, val in schema['properties'].items():
        if val.get('type') == 'object':
            rows = process_object(schema, key, val, rows)
        elif val.get('type') == 'array':
            rows = process_array(schema, key, val, rows)
        else:
            rows = process_primitive(schema, key, val, rows)
    for key, val in schema['definitions'].items():
        rows.append(['','','','',''])
        rows = process_object(schema, key, val, rows)

    with open(path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def process_object(schema, name, entry, rows, nesting='', required=''):
    required = 'Required' if name in schema['required'] + entry.get('required', [])  else required
    if not entry.get('properties'):
        rows.append([nesting + name, 'object', None, required, entry.get('description')])
        return rows
    rows.append((nesting + name, 'object', None, required, entry.get('description')))
    nesting += '{}/'.format(name)
    for key, val in entry['properties'].items():
        if val.get('type') == 'object':
            rows = process_object(schema, key, val, rows, nesting)
        elif val.get('type') == 'array':
            rows = process_array(schema, key, val, rows, nesting)
        elif val.get("$ref"):
            rows.append([nesting + val['$ref'], val['$ref'], None, None, None])
        else:
            rows = process_primitive(schema, key, val, rows, nesting)
    return rows

def process_array(schema, key, array, rows, nesting='', required=''):
    required = 'Required' if key in schema['required'] else required
    if array['items'].get('$ref'):
        rows[-1] = [nesting + key, 'array({})'.format(array['items']['$ref']), None, required, array.get('description')]
    elif array['items'].get('type') == 'object':
        nesting += '{}/'.format(key)
        rows = process_object(schema, '', array['items'], rows, nesting)
    elif array['items'].get('anyOf'):
        rows[-1] = [nesting + key, 'array({})'.format(','.join(ref['$ref'] for ref in array['items']['anyOf'])), None, required, array.get('description')]
    else:
        rows.append([nesting + key, 'array({})'.format(array['items'].get('type')), rfc_map(array['items'].get('format', '')), is_required(schema, key), array.get('description')])
    return rows

def rfc_map(format):
    return {
        'uri': 'RFC3987',
        'date-time': 'RFC3339',
        'date': 'ISO8601'
    }.get(format, '')

def is_required(schema, name):
    return 'Required' if name in schema['required'] else ''

def process_primitive(schema, key, prim, rows, nesting='', required=''):
    rows.append((nesting + key, prim.get('type'), rfc_map(prim.get('format', '')), is_required(schema, key), prim.get('description')))
    return rows

if __name__ == '__main__':
    main()
