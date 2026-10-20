#!/usr/bin/env python3
"""Verify the byte-for-byte BrandRadar baseline, without external dependencies.

This is an import integrity check, not a regression test after adaptation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'docs/upstream/import-manifest.json').read_text())
    entries = manifest['files']
    errors = []
    destinations = set()
    sources = set()
    for entry in entries:
        relative = Path(entry['destination_path'])
        if relative.is_absolute() or '..' in relative.parts:
            errors.append(f'Unsafe destination: {relative}')
            continue
        if str(relative) in destinations or entry['source_path'] in sources:
            errors.append(f'Duplicate manifest entry: {relative}')
        destinations.add(str(relative))
        sources.add(entry['source_path'])
        path = root / relative
        if not path.is_file():
            errors.append(f'Missing: {relative}')
            continue
        data = path.read_bytes()
        digest = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        if digest != entry['sha']:
            errors.append(f'Modified: {relative}')
    if len(entries) != manifest['file_count']:
        errors.append('Manifest count mismatch')
    if errors:
        print('\n'.join(errors))
        print('Baseline differs. If adapting source files, review changes against the import commit.')
        return 1
    print(f"OK: {len(entries)} upstream files match {manifest['source_commit']} byte-for-byte")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
