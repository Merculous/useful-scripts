#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import tarfile
# import time
from argparse import ArgumentParser

# TODO
# Use out path when True

# TODO
# Custom extract which will use the correct parameters to peform
# an easy extract, no arguments needed?

# TODO
# If we are using more than archiver that requires tar, don't
# keep deleting the {}.tar file so we don't keep removing
# and use the same one.

# TODO
# Freearc
# GrZip
# zlib?

# TODO
# Differ path in which users folder is located with its contents,
# and when there's more than one file with the same "basename",
# get each file's size and remove all but the smallest one.

# TODO
# Better timimg logging
# Progress bar

# TODO
# Different operations between being passed a file and a directory

# TODO
# Function to use top 3 archivers

'''
toolbar_width = 40

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

for i in xrange(toolbar_width):
    time.sleep(0.1) # do real work here
    # update the bar
    sys.stdout.write("-")
    sys.stdout.flush()

sys.stdout.write("]\n") # this ends the progress bar
'''


class Tar(object):
    def __init__(self, path: str, out=False):
        super().__init__()

        # TODO Make sure below works, it should already

        if '.tar' in path:
            self.path = path.split('.tar')[0]
        else:
            self.path = path

        self.out = out

    def makeCompressedTar(self, alg: str) -> None:
        stuff = {
            'bzip2': {
                'mode': 'w:bz2',
                'name': '{}.tar.bz2'.format(self.path)
            },
            'gzip': {
                'mode': 'w:gz',
                'name': '{}.tar.gz'.format(self.path)
            },
            'xz': {
                'mode': 'w:xz',
                'name': '{}.tar.xz'.format(self.path)
            }
        }

        if alg not in stuff:
            sys.exit('Unsupported alg: {}'.format(alg))

        with tarfile.open(stuff[alg]['name'], stuff[alg]['mode']) as f:
            print('Creating compressed tar with: {}'.format(alg))
            f.add(self.path)
            f.close()

        if os.path.exists(stuff[alg]['name']):
            print('Successfully created tar: {}'.format(stuff[alg]['name']))
        else:
            raise FileNotFoundError('We failed to create tar!')

    def makeRawTar(self) -> None:
        name = '{}.tar'.format(self.path)
        with tarfile.open(name, 'w') as f:
            print('Creating tar file: {}'.format(name))
            f.add(self.path)
            f.close()

        if os.path.exists(name):
            print('Sucessfully created tar: {}'.format(name))
        else:
            raise FileNotFoundError('We failed to create tar!')


class Compress(object):
    def __init__(self, path: str, out=False):
        super().__init__()

        self.path = path
        self.out = out  # TODO

        if os.path.isdir(self.path):
            self.dir = True
        else:
            self.dir = False

    def bsc(self, keep=True) -> None:
        name = '{}.tar'.format(self.path)

        if not keep:
            if os.path.exists(name):
                os.remove(name)

        if self.dir:
            t = Tar(self.path)
            t.makeRawTar()

        cmd = (
            shutil.which('bsc'),
            'e',
            name,
            '{}.bsc'.format(name),
            '-b1024',
            '-e2'
        )

        subprocess.run(cmd)

        os.remove(name)

    def nanozip(self) -> None:
        cmd = (
            'nz',
            'a',
            '-cc',
            '-m8g',
            '-r',
            '-t16',
            '{}.nz'.format(self.path),
            self.path
        )

        subprocess.run(cmd)

    def pcompress(self, keep=True) -> None:
        name = '{}.tar'.format(self.path)

        if not keep:
            if os.path.exists(name):
                os.remove(name)

        if self.dir:
            t = Tar(self.path)
            t.makeRawTar()

        cmd = (
            shutil.which('pcompress'),
            '-c',
            'adapt2',
            '-l14',
            '-L',
            '-s1g',
            name
        )

        subprocess.run(cmd)

        os.remove(name)

    def precomp(self, keep=True) -> None:
        name = '{}.tar'.format(self.path)

        if not keep:
            if os.path.exists(name):
                os.remove(name)

        if self.dir:
            t = Tar(self.path)
            t.makeRawTar()

        cmd = (
            shutil.which('precomp'),
            '-cl',
            '-lm8192',
            '-e',
            name
        )

        subprocess.run(cmd)

        os.remove(name)

    def p7zip(self) -> None:
        cmd = (
            shutil.which('7za'),
            'a',
            '-t7z',
            '-m0=lzma2',
            '-mx=9',
            '-aoa',
            '-md128m',
            '-mfb273',
            '-ms16g',
            '-mmt4',
            '-ms=on',
            '{}.7z'.format(self.path),
            self.path
        )

        subprocess.run(cmd)

    def zpaq(self) -> None:
        cmd = (
            shutil.which('zpaq'),
            'a',
            '{}.zpaq'.format(self.path),
            self.path,
            '-method',
            str(6)
        )

        subprocess.run(cmd)


def doAll(path: str) -> None:
    c = Compress(path)
    t = Tar(path)

    c.bsc()
    t.makeCompressedTar('bzip2')
    t.makeCompressedTar('gzip')
    c.nanozip()
    c.precomp(False)
    c.pcompress(False)
    c.p7zip()
    t.makeCompressedTar('xz')
    c.zpaq()


# TODO
# Ensure this works with multiple differently named files, rather than just one

def diffAndLeaveSmallest(path: str) -> None:
    files = list()

    for stuff in os.listdir(path):
        if os.path.isfile(stuff):
            files.append(stuff)

    if files:
        if len(files) > 2:
            for garbage in files:
                if os.path.isdir(garbage):
                    files.remove(garbage)

            compare = list()

            extensions = (
                'bsc', 'bz2', 'gz',
                'nz', 'pcf', 'pz',
                '7z', 'xz', 'zpaq'
            )

            for match in extensions:
                for file in files:
                    if file.endswith(match):
                        size = os.path.getsize(file)
                        compare.append((file, size))

            tmp = list()

            for name, size in compare:
                tmp.append(size)

            smallest = min(tmp)

            remove = list()

            for name, size in compare:
                if size == smallest:
                    print('{} is the smallest file!'.format(name))
                else:
                    remove.append(name)

            for file in remove:
                print('Removing: {}'.format(file))
                os.remove(file)
        else:
            sys.exit('Only one file exists, nothing to do!')
    else:
        sys.exit('No files to diff!')


def extract(path: str, out=False) -> None:
    pass


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('-i', nargs=1, metavar='\b')
    parser.add_argument('-o', nargs=1, metavar='\b')

    parser.add_argument('--all',        action='store_true')
    parser.add_argument('--bsc',        action='store_true')
    parser.add_argument('--bzip2',      action='store_true')
    parser.add_argument('--gzip',       action='store_true')
    parser.add_argument('--nanozip',    action='store_true')
    parser.add_argument('--precomp',    action='store_true')
    parser.add_argument('--pcompress',  action='store_true')
    parser.add_argument('--p7zip',      action='store_true')
    parser.add_argument('--xz',         action='store_true')
    parser.add_argument('--zpaq',       action='store_true')

    parser.add_argument('--diff',       action='store_true')

    args = parser.parse_args()

    if args.i:

        c = Compress(args.i[0])
        t = Tar(args.i[0])

        if args.all:
            doAll(args.i[0])

        elif args.bsc:
            c.bsc()

        elif args.bzip2:
            t.makeCompressedTar('bzip2')

        elif args.gzip:
            t.makeCompressedTar('gzip')

        elif args.nanozip:
            c.nanozip()

        elif args.precomp:
            c.precomp()

        elif args.pcompress:
            c.pcompress()

        elif args.p7zip:
            c.p7zip()

        elif args.xz:
            t.makeCompressedTar('xz')

        elif args.zpaq:
            c.zpaq()

        elif args.diff:
            diffAndLeaveSmallest(args.i[0])

        else:
            sys.exit('Please select an action!')

    else:
        sys.exit(parser.print_help(sys.stderr))


if __name__ == '__main__':
    main()
