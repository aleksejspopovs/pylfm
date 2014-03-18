#!/usr/bin/env python3
import os
import sys
import pickle
from difflib import get_close_matches

from mutagenx.flac import FLAC
from mutagenx.easyid3 import EasyID3

from lfm import LastFM
from lfm import try_really_hard as trh

def choose(lst, perfect, msg):
    if len(lst) == 0:
        return None

    if (len(lst) == 1) or (lst[0] == perfect):
        return lst[0]

    print(msg, file=sys.stderr)
    print(lst, file=sys.stderr)

    n = None
    try:
        n = int(input())
    except ValueError:
        return None

    if (n < 0) or (n >= len(lst)):
        return None

    return lst[n]

API_KEY = '3166d15f23de42305e82a2c2c3e8df99'

if len(sys.argv) < 3:
    print('USAGE:')
    print('{} username dir1 [dir2 [dir3 …]]'.format(sys.argv[0]))
    sys.exit()

lfm = LastFM(API_KEY)

username = sys.argv[1]
dirs = sys.argv[2:]
picklename = 'local-lib.pickle'

if dirs[0].endswith('pickle'):
    picklename = dirs.pop(0)
    local = pickle.load(open(picklename, 'rb'))
else:
    local = {}

# first, collect data from the local collection
for d in dirs:
    for dirpath, dirnames, filenames in os.walk(d):
        print('Scanning {}'.format(dirpath), file=sys.stderr)
        for f in filenames:
            path = os.path.join(dirpath, f)
            track = None
            if f.lower().endswith('.mp3'):
                try:
                    track = EasyID3(path)
                except:
                    continue
            if f.lower().endswith('.flac'):
                try:
                    track = FLAC(path)
                except:
                    continue

            if track is not None:
                try:
                    artist, album, title = track['artist'][0], track['album'][0], track['title'][0]
                except KeyError:
                    continue
                artist, album, title = artist.lower(), album.lower(), title.lower()

                if artist not in local:
                    local[artist] = {}
                if album not in local[artist]:
                    local[artist][album] = {}
                if title not in local[artist][album]:
                    local[artist][album][title] = [path]
                else:
                    local[artist][album][title].append(path)

pickle.dump(local, open(picklename, 'wb'))

tracks = lfm.get_user_loved_tracks(username)
print('Found {n} tracks loved by {u}.'.format(u=username, n=len(tracks)), file=sys.stderr)

not_found = []

for artist, title in tracks:
    artist, title = artist.lower(), title.lower()
    file_candidates = []
    for a in get_close_matches(artist, local):
        for album, tracks in local[a].items():
            for track in get_close_matches(title, tracks):
                for f in local[a][album][track]:
                    file_candidates.append(f)


    f = choose(file_candidates, None, 'Choose file for {}'.format((artist, title)))
    if f is None:
        not_found.append((artist, title))
        continue

    print(f)

print('Done, {} tracks not found.'.format(len(not_found)), file=sys.stderr)
print(not_found, file=sys.stderr)
