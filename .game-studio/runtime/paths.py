"""Repository-confined paths. Reject links and Windows reparse points."""
import hashlib
import os
import stat
from pathlib import Path, PurePosixPath


def plain(path):
    path = Path(path).absolute()
    for part in [*reversed(path.parents), path]:
        try:
            entry = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(entry.st_mode) or getattr(entry, 'st_file_attributes', 0) & 1024:
            raise ValueError(f'Link/reparse path is not supported: {part}')
    return path.resolve(strict=False)


def relative_parts(relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ValueError(f'Unsafe relative path: {relative!r}')
    p = PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts or relative.startswith('/'):
        raise ValueError(f'Unsafe relative path: {relative!r}')
    return p.parts


def confined(root, relative):
    parts = relative_parts(relative)
    root = plain(root)
    target = plain(root.joinpath(*parts))
    if not target.is_relative_to(root):
        raise ValueError(f'Path escapes repository: {relative}')
    return target


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f'.studio-{os.getpid()}.tmp')
    created = False
    try:
        with temp.open('xb') as f:
            created = True
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if created and temp.exists():
            temp.unlink()
