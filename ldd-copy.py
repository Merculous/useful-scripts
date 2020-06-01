#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

argv = sys.argv


def getLibsFromFile(file, path):
    if os.path.isfile(file):
        # Get outputted libraries from ldd
        cmd = subprocess.run((
            'ldd',
            file),
            stdout=subprocess.PIPE,
            universal_newlines=True)
        files = cmd.stdout.splitlines()
        for stuff in files:
            orig = stuff.split('(')
            new = orig[0].strip()
            if '=>' in new:
                # tmp is a list, 0 name of object/symlink, 1 path of used object
                tmp = new.replace(' =>', '').split(' ')
                # Fix path because most are symlinks, os.path.realpath will fix this
                tmp[1] = os.path.realpath(tmp[1])
                print('Copying object: {}'.format(tmp[1]))
                shutil.copy(tmp[1], '{}/{}'.format(path, tmp[0]))
    else:
        raise IOError('{} is not a file!'.format(argv[2]))

    if os.path.isdir(path):
        print('Saving to directory: {}'.format(path))
    else:
        raise IOError('{} is not a directory!'.format(argv[3]))


def main():

    parser = argparse.ArgumentParser(usage='{} <file> <dir>'.format(argv[0]))

    parser.add_argument('-i', nargs=2, metavar=('FILE', 'DIR'))

    args = parser.parse_args()

    if args.i:
        getLibsFromFile(argv[2], argv[3])
    else:
        sys.exit(parser.print_help(sys.stderr))


if __name__ == '__main__':
    main()
