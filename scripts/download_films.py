"""Download the six edition-01 films and verify their SHA-256 checksums."""

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='Check existing files without downloading.')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'verification/visuals-edition-01.json').read_text(encoding='utf-8'))
    for film in manifest['films']:
        target = ROOT / film['path']
        if not target.exists():
            if args.verify_only:
                raise SystemExit(f'Missing film: {film["path"]}')
            target.parent.mkdir(parents=True, exist_ok=True)
            partial = target.with_suffix('.mp4.partial')
            print(f'Downloading {film["asset"]} ({film["bytes"] / 2**20:.1f} MiB)', flush=True)
            request = urllib.request.Request(film['url'], headers={'User-Agent': 'Sixfold-archive'})
            with urllib.request.urlopen(request, timeout=120) as response, partial.open('wb') as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            if partial.stat().st_size != film['bytes'] or digest(partial) != film['sha256']:
                partial.unlink()
                raise SystemExit(f'Checksum mismatch: {film["asset"]}')
            partial.replace(target)
        if target.stat().st_size != film['bytes'] or digest(target) != film['sha256']:
            raise SystemExit(f'Existing film differs from the archive: {film["path"]}')
        print(f'PASS {film["asset"]}', flush=True)


if __name__ == '__main__':
    main()
