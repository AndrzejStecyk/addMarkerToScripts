#!/usr/bin/python3.4
import shutil
from pathlib import Path


def add_line(file_path, content, line):
    content.insert(1, line + '\n')
    with open(file_path, 'w') as frp:
        content = "".join(content)
        frp.write(content)


def add_marker(file):
    file_path = str(file.absolute())
    sh = ['#!/bin/bash', '#!/bin/sh']
    sh_line = "echo $(date '+%Y%m%d%H%M%S') module=$(readlink -f $0) pid=$$ host=$(uname -n)"

    py = 'python'
    py_line = 'import os\n' \
              'os.system("echo $(date \'+%Y%m%d%H%M%S\') module="+os.path.abspath(__file__)+" pid=$$ host=$(uname -n)")'

    pl = 'perl'
    pl_line = 'system("echo \$(date \'+%Y%m%d%H%M%S\') module=\$(readlink -f $0) pid=\$\$ host=\$(uname -n)");'

    with open(file_path, 'r') as fp:
        content = fp.readlines()

    if len(content) > 0:
        print(content[0])
        if content[0].strip() in sh:
            add_line(file_path, content, sh_line)
        elif py in content[0].strip().lower():
            add_line(file_path, content, py_line)
        elif pl in content[0].strip().lower():
            add_line(file_path, content, pl_line)


def make_backup(file):
    dest = Path(str(file.absolute()) + '_python_bac')
    if dest.exists():
        raise FileExistsError("make_backup", "Can't copy a file, backup already exists")

    shutil.copy(file, dest)

    if not dest.exists():
        raise FileNotFoundError("make_backup", "Could not create a backup")


if __name__ == '__main__':
    base = Path("Z:/tmp")
    extensions = ['.sh', '.py', '.pl']
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
