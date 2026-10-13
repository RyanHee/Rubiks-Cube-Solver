"""Print the orientation codes for every mapped piece."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    for kind in ('corner', 'edge'):
        mapping_path = PROJECT_ROOT / 'data' / f'{kind}_mapping.json'
        mapping = json.loads(mapping_path.read_text())
        print(f'{kind.capitalize()} mapping:')
        for letters, position in mapping['Position'].items():
            codes = [mapping['Orientation'][letter] for letter in letters]
            print(position, ':', codes)


if __name__ == '__main__':
    main()
