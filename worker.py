import time
import sys
import argparse
import datetime
sys.path.append("libs/")
import core_engine

# python worker.py 18:00 daily 5
## Creates playlists for all users every day at 18:00
## Each playlist has 5 musics

def valid_time(s):
    try:
        return datetime.strptime(s, "%Y:%m:%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description="Worker to create playlists for each user.")
parser.add_argument('-t',"--time", metavar='HH:MM:SS', type=valid_time, help='the time for the worker to create playlists. format - HH:MM:SS', required=True)
parser.add_argument('--periodicity', nargs='+', required=True, help='create playlists daily')
parser.add_argument('--weekly', help='create playlists weekly')
parser.add_argument('--monthly', help='create playlists monthly')
args = parser.parse_args()
print(args.accumulate(args.integers))