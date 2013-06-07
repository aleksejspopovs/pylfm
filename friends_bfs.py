#!/usr/bin/env python3
import sys
import json
import pickle
from lfm import LastFM
from lfm import try_really_hard as trh

API_KEY = '3166d15f23de42305e82a2c2c3e8df99'

if len(sys.argv) != 3:
	print('USAGE:')
	print('{} username levels'.format(sys.argv[0]))
	sys.exit()

lfm = LastFM(API_KEY)

username = sys.argv[1]
levels = int(sys.argv[2])

print('Fetching {u}\'s friends {l} levels deep.'.format(u=username, l=levels))

friends = [[username]]
seen = set([username])
for i in range(1, levels + 1):
	this_level = []
	for prev in friends[-1]:
		for friend in lfm.get_user_friends(prev):
			if friend not in seen:
				seen.add(friend)
				this_level.append(friend)
	friends.append(this_level)
	print('Level {i}/{t} finished, {c} friends found.'.format(i=i, t=levels, c=len(this_level)))

pickle.dump(friends, open('lastfm-friends-{}.bin'.format(username), 'wb'))
json.dump(friends, open('lastfm-friends-{}.json'.format(username), 'w'))

print('Done.'.format(n=len(friends)))
