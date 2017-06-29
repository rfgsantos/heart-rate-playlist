import argparse
import datetime, time, threading
import sys
sys.path.append("libs/")
import core_engine

# python worker.py --daily --size 5

MONTH_DELTA = 2592000
WEEK_DELTA = 604800
DAY_DELTA = 86400

def valid_time(s):
    try:
        return datetime.datetime.strptime(s, "%H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description="Worker to create playlists for all users.")
#parser.add_argument('time', metavar='HH:MM:SS', type=valid_time, help='Time at which to create playlists. (format - HH:MM:SS)')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--daily', action="store_true", help="Create playlists daily.")
group.add_argument('--weekly', action="store_true", help="Create playlists weekly.")
group.add_argument('--monthly', action="store_true", help="Create playlists month.")

parser.add_argument('-s', '--size', action="store", type=int, default=10, help="Size of the playlists to be created.", required=True)

args = parser.parse_args()
<<<<<<< HEAD

def sleep_until(time):
    pass

def create_playlist(delta):
    start = time.time()
    print(time.ctime())
    ## GET ALL USERS
    ## FOR EACH USER GET REACTIONS
    processor = core_engine.Processor()
    users = processor.get_users()
    for user in users:
        reactions = user.reactions()
        seed = reactions.positive() #analyses duration for positive classification
        recommendations = processor.create_recommendations(seed)
        processor.create_playlist(user, recommendations)
    ## FILTER GOOD REACTIONS
    ## RECOMMEND FROM GOOD REACTION
    ## CREATE PLAYLIST
    end = time.time()
    runtime = end - start
    sleep = delta - runtime
    threading.Timer(sleep, create_playlist, [delta]).start()

if __name__ == "__main__":
    now = datetime.datetime.now()
    if args.daily:
        delta = DAY_DELTA
    elif args.week:
        delta = WEEK_DELTA
    elif args.month:
        delta = MONTH_DELTA
    else:
        print("Wrong periodic input.")
        exit(1)
    delta = 10
    create_playlist(delta)
=======
print(args.accumulate(args.integers))

def func():
    processor = core_engine.Processor()
    users = processor.get_users()
    for user in users:
        reactions = user.reactions()
        seed = reactions.positive() #analyses duration for positive classification
        recommendations = processor.create_recommendations(seed)
        processor.create_playlist(user, recommendations)
    del(processor)
>>>>>>> 784bfdd42bba44a1618baa8cae416cb44ae87c3e
