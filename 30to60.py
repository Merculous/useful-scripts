#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

cwd = os.getcwd()

if 'converted' not in os.listdir(cwd):
    print('Creating folder for converted videos.')
    os.mkdir('converted')


def checkForDups():
    garbage = list()
    videos = list()
    duplicate = list()

    for stuff in os.listdir(cwd):
        if os.path.isfile(stuff):
            if stuff.endswith('mp4'):
                videos.append(stuff)
            else:
                garbage.append(stuff)
        else:
            garbage.append(stuff)

    os.chdir('converted')  # This can be done better

    for shit in os.listdir(cwd):
        if os.path.isfile(shit):
            if shit.endswith('mp4'):
                videos.append(shit)
            else:
                garbage.append(shit)
        else:
            garbage.append(shit)

    for video in videos:
        if videos.count(video) > 1:
            if video not in duplicate:
                duplicate.append(video)

    if not duplicate:
        sys.exit('There are no duplicates!')
    else:
        print('Duplicate: ./{}'.format(' '.join(duplicate)))


def convert(video):
    video = os.path.abspath(video)
    try:
        ffmpeg_location = subprocess.run((
            'which', 'ffmpeg'),
            stdout=subprocess.PIPE, universal_newlines=True)
    except:
        raise FileNotFoundError

    parameters = [
        ffmpeg_location.stdout.strip(),
        "-i {}".format(video),
        "-c:v libx264",
        "-preset fast",
        "-x264opts nal-hrd=cbr:force-cfr=1",
        "-b:v 6M",
        "-minrate 6M",
        "-maxrate 6M",
        "-bufsize 6M",
        "-c:a copy",
        "-r 60",
        "-force_fps",
        "-aspect 16:9",
        "-s 1280x720",
        "-vf minterpolate=fps=60:mi_mode=mci:mc_mode=obmc:me_mode=bilat:me=epzs:mb_size=16:search_param=32:scd=fdiff:scd_threshold=5",
        "-metadata comment=' '",
        "converted/{}".format(os.path.basename(video))
    ]

    subprocess.run(' '.join(parameters).strip(), shell=True)


def main():
    argv = sys.argv
    parser = argparse.ArgumentParser(
        usage='{} <option> <arg>'.format(argv[0]))
    parser.add_argument(
        '-c', help='convert a video', nargs=1, metavar='VIDEO')
    parser.add_argument(
        '-d', help='checks for duplicates', action='store_true')
    args = parser.parse_args()

    if args.c:
        convert(argv[2])
    elif args.d:
        checkForDups()
    else:
        sys.exit(parser.print_help(sys.stderr))


if __name__ == '__main__':
    main()
