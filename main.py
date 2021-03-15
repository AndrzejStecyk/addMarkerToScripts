#!/usr/bin/python3.4
import shutil
from pathlib import Path


def add_marker(file):
    sh = ['#!/bin/bash', '#!/bin/sh']
    sh_str = "echo $(date '+%Y%m%d%H%M%S') module=$(readlink -f $0) pid=$$ host=$(uname -n)"
    with open(str(file.absolute()), 'r') as fp:
        content = fp.readlines()

    if len(content) > 0:
        print(content[0])
        if content[0].strip() in sh:
            content.insert(1, sh_str + '\n')
            with open(str(file.absolute()), 'w') as frp:
                content = "".join(content)
                frp.write(content)


def make_backup(file):
    dest = Path(str(file.absolute()) + '_python_bac')
    if dest.exists():
        raise FileExistsError("make_backup", "Can't copy a file, backup already exists")

    shutil.copy(file, dest)

    if not dest.exists():
        raise FileNotFoundError("make_backup", "Could not create a backup")


if __name__ == '__main__':
    base = Path("Z:/tmp")
    extensions = ['.sh']
    for somefile in base.glob('**/*'):
        if somefile.suffix in extensions:
            try:
                make_backup(somefile)
            except FileExistsError:
                continue
                # TODO

            except FileNotFoundError:
                continue
                # TODO

            add_marker(somefile)
