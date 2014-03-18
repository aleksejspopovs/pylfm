#!/usr/bin/env python3
import sys
import json
import pickle
from lfm import LastFM
from lfm import try_really_hard as trh

API_KEY = '3166d15f23de42305e82a2c2c3e8df99'

if len(sys.argv) != 3:
    print('USAGE:')
    print('{} user1 user2'.format(sys.argv[0]))
    sys.exit()

lfm = LastFM(API_KEY)

user1, user2 = sys.argv[1:]

shouts = [x for x in lfm.get_user_shouts(user1) if x[1] == user2]
if user1 != user2:
    shouts += [x for x in lfm.get_user_shouts(user2) if x[1] == user1]

shouts.sort()
for shout in shouts:
    print(shout[0].isoformat(), shout[1])
    print(shout[2])
    print()
