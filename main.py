import csv
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
        gen_docs(schema, args.docs)
    if args.validate:
        if validate(schema, args.test):
            print("{}.yaml validated against {}.json".format(args.yaml_path, args.test))


def parse_args():
    parser = argparse.ArgumentParser(description="A command line interface for schema things")

    parser.add_argument('--test', dest='test', type=str, help='The name of the test json file', default='test')
    parser.add_argument('--yaml', dest='yaml_path', type=str, help='The name of the yaml schema file', default='share')
    parser.add_argument('-d', '--dest', dest='dest', type=str, help='The name of the desired json output file', default='schema')
    parser.add_argument('--docs', dest='docs', type=str, help='The full path (extension included) to the desired location for documentation', default='')
    parser.add_argument('-v', '--validate', dest='validate', help='A flag to validate the schema against a test file', action='store_true')

    return parser.parse_args()


def get_json_schema(yaml_path):
    with open(yaml_path + '.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=Loader)


def validate(schema, path):
    with open(path + '.json', 'r') as f:
        test = json.load(f)

    format_checker = jsonschema.FormatChecker(formats=jsonschema.FormatChecker.checkers.keys())
    return jsonschema.validate(test, schema, format_checker=format_checker) is None


def write_to_json(schema, path):
    with open(path + '.json', 'w') as f:
        f.write(json.dumps(schema, indent=4))

def gen_docs(schema, path):
    rows = [('name', 'type', 'format', 'description')]
    for key, val in schema['properties'].items():
        if val.get('type') == 'object':
            rows = process_object(schema, key, val, rows)
        elif val.get('type') == 'array':
            rows = process_array(schema, key, val, rows)
        elif val.get('$ref'):
            process_ref(schema, val['ref'], rows, nesting)
        else:
            rows = process_primitive(schema, key, val, rows)


    with open(path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def gen_row(schema, key, val):
    rfc_map = {
        'uri': 'RFC3987',
        'date-time': 'RFC3339',
        'date': 'ISO8601'
    }
    type_ = val.get('type')
    format = val.get('format', '')
    description = val.get('description')

    if type_ == 'array':
        return gen_array(schema, key, val)
    elif type_ == 'object':
        return gen_object(schema, key, val)

    return (key, type_, rfc_map.get(format), description)

def process_object(schema, name, entry, rows, nesting=''):
    rows.append((nesting + name, 'object', None, entry.get('description')))
    nesting += '{}/'.format(name)
    for key, val in entry['properties'].items():
        if val['type'] == 'object':
            rows = process_object(schema, key, val, rows, nesting)
        elif val['type'] == 'array':
            rows = process_array(schema, key, val, rows, nesting)
        else:
            rows = process_primitive(schema, key, val, rows, nesting)
    return rows

def process_array(schema, key, array, rows, nesting=''):
    rows.append((nesting + key, 'array', None, array.get('description')))
    nesting += 'items/'
    if array['items'].get('$ref'):
        rows = process_ref(schema, array['items']['$ref'], rows, nesting)
    return rows

def process_ref(schema, ref, rows, nesting):
    return rows

def process_primitive(schema, key, prim, rows, nesting=''):
    rfc_map = {
        'uri': 'RFC3987',
        'date-time': 'RFC3339',
        'date': 'ISO8601'
    }
    rows.append((nesting + key, prim.get('type'), rfc_map.get(prim.get('format', '')), prim.get('description')))
    return rows

if __name__ == '__main__':
    main()
