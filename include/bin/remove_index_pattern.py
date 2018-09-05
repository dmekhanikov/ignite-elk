import json
import sys


def find_index(patterns, regex):
    for (i, pattern) in enumerate(patterns):
        if pattern['es']['default_index'] == regex:
            return i

    return -1


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        data = json.load(f)
        patterns = data['index_patterns']
        for regex in sys.argv[2:]:
            idx = find_index(patterns, regex)
            if idx == -1:
                print("Index pattern {} was not found".format(regex))
            else:
                del patterns[idx]

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
