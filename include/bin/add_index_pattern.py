import copy
import json
import sys


def add_pattern(data, regex):
    patterns = data['index_patterns']
    new_pattern = copy.deepcopy(patterns[0])
    new_pattern['es']['default_index'] = regex
    patterns.append(new_pattern)


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        data = json.load(f)
        for regex in sys.argv[2:]:
            add_pattern(data, regex)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
