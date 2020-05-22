#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys


def compress(data, alg):
    data = os.path.abspath(data)

    if alg == 'xz':
        env = os.environ['XZ_OPT'] = '-e9'
        print('XZ_OPT environment variable is:{}'.format(env))
        subprocess.run([
            'tar',
            'cvJf',
            '{}.txz'.format(data),
            data])

    elif alg == '7z':
        subprocess.run([
            '7za',
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
            '{}.7z'.format(data),
            data])

    elif alg == 'zpaq':
        subprocess.run([
            'zpaq',
            'a',
            '{}.zpaq'.format(data),
            data,
            '-method',
            '5'])  # Some can have 6 but I'll just leave it cause I'm too lazy to add another whole command

    else:
        raise ValueError('Algorithm {} is not supported!'.format(alg))


def main():
    argv = sys.argv

    parser = argparse.ArgumentParser(usage='{} <alg> <path>'.format(argv[0]))

    parser.add_argument('--xz', nargs=1, help='Use xz', metavar='PATH')
    parser.add_argument('--p7z', nargs=1, help='Use 7zip', metavar='PATH')
    parser.add_argument('--zpaq', nargs=1, help='Use zpaq', metavar='PATH')

    args = parser.parse_args()

    if args.xz:
        print('Compressing with xz...')
        compress(argv[2], 'xz')

    elif args.p7z:
        print('Compressing with 7zip')
        compress(argv[2], '7z')

    elif args.zpaq:
        print('Compresssing with zpaq...')
        compress(argv[2], 'zpaq')

    else:
        sys.exit(parser.print_help(sys.stderr))


if __name__ == '__main__':
    main()
