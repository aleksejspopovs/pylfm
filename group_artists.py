#!/usr/bin/env python3
import last
import sys
from last import LastFM
from last import try_really_hard as trh

API_KEY = '3166d15f23de42305e82a2c2c3e8df99'

if len(sys.argv) != 2:
	print('USAGE:')
	print('{} groupname'.format(sys.argv[0]))
	sys.exit()

lfm = LastFM(API_KEY)

groupname = sys.argv[1]
members = trh(lambda: lfm.get_group_members(groupname))

print('Found {cnt} members of group "{grp}".'.format(grp=groupname, cnt=len(members)))

artists = {}
for i, user in enumerate(members):
	here = trh(lambda: lfm.get_user_artists(user))
	for a in here:
		if a[0] in artists:
			artists[a[0]].append((user, a[1]))
		else:
			artists[a[0]] = [(user, a[1])]
	print('[{i}/{total}] User {user} processed, {n} artists found.'.format(
		i=i + 1,
		total=len(members),
		user=user,
		n=len(here)
	))

for a in artists:
	artists[a].sort(key=lambda x: x[1])

pickle.dump(artists, open('lastfm-data-{}.bin'.format(groupname), 'wb'))
json.dump(artists, open('lastfm-data-{}.json'.format(groupname), 'w'))

print('Done, {n} artists found in total.'.format(n=len(artists)))
