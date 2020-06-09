#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys
import time


def compress(data, alg):
    if alg == 'xz':
        try:
            tar_location = subprocess.run(
                ('which', 'tar'), stdout=subprocess.PIPE, universal_newlines=True)
        except:
            raise FileNotFoundError

        env = os.environ['XZ_OPT'] = '-e9'
        commands = (
            tar_location.stdout.strip(), 'cvJf',
            '{}.txz'.format(data), data)
        subprocess.run(commands)

    elif alg == '7z':
        try:
            p7z_location = subprocess.run(
                ('which', '7za'), stdout=subprocess.PIPE, universal_newlines=True)
        except:
            raise FileNotFoundError

        commands = (
            p7z_location.stdout.strip(), 'a', '-t7z', '-m0=lzma2', '-mx=9', '-aoa', '-md128m',
            '-mfb273', '-ms16g', '-mmt4', '-ms=on', '{}.7z'.format(data), data)
        subprocess.run(commands)

    elif alg == 'zpaq':
        try:
            zpaq_location = subprocess.run(
                ('which', 'zpaq'), stdout=subprocess.PIPE, universal_newlines=True)
        except:
            raise FileNotFoundError

        commands = (
            zpaq_location.stdout.strip(), 'a', '{}.zpaq'.format(
                data), data, '-method', '5')
        subprocess.run(commands)

    else:
        raise ValueError('Algorithm {} is not supported!'.format(alg))


def main():
    argv = sys.argv

    parser = argparse.ArgumentParser(usage='{} <alg> <path>'.format(argv[0]))

    parser.add_argument(
        '--xz', nargs=1, help='Use xz (slow, good compression, on basically every device at this point)', metavar='PATH')
    parser.add_argument(
        '--p7z', nargs=1, help='Use 7zip (fast, great compression, needs to be downloaded)', metavar='PATH')
    parser.add_argument(
        '--zpaq', nargs=1, help='Use zpaq (fast, best compression, needs to be downloaded)', metavar='PATH')

    args = parser.parse_args()

    if args.xz:
        print('Compressing with xz...')
        start = time.time()
        compress(argv[2], 'xz')
        end = time.time() - start
        print('xz took {:.2f} seconds'.format(end))

    elif args.p7z:
        print('Compressing with 7zip...')
        start = time.time()
        compress(argv[2], '7z')
        end = time.time() - start
        print('7zip took {:.2f} seconds'.format(end))

    elif args.zpaq:
        print('Compressing with zpaq...')
        start = time.time()
        compress(argv[2], 'zpaq')
        end = time.time() - start
        print('zpaq took {:.2f} seconds'.format(end))

    else:
        sys.exit(parser.print_help(sys.stderr))


if __name__ == '__main__':
    main()
