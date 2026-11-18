"""Verify every committed visualisation source and asset against the edition manifest."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'verification/visuals-edition-01.json').read_text(encoding='utf-8'))
    for entry in manifest['files']:
        path = ROOT / entry['path']
        with path.open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if path.stat().st_size != entry['bytes'] or actual != entry['sha256']:
            raise SystemExit(f'Archive mismatch: {entry["path"]}')
    library = ROOT / manifest['library']
    recipe = json.loads((library / 'source/manifest.json').read_text(encoding='utf-8'))
    if len(recipe['stills']) != 100 or len(manifest['films']) != 6:
        raise SystemExit('Expected 100 still compositions and six films.')
    for item in recipe['stills']:
        for kind in ['image', 'master', 'thumbnail']:
            if not (library / item[kind]).is_file():
                raise SystemExit(f'Missing {kind} for {item["id"]}')
    print(f'PASS {len(manifest["files"])} files; all 100 JPEGs, PNG masters and thumbnails are present.')
    print('Film hashes are recorded; run scripts/download_films.py to retrieve and verify the six MP4s.')


if __name__ == '__main__':
    main()
