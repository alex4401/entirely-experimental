# asbnames.py FILE

import sys
import json

fname = sys.argv[1]

with open(fname, 'r') as fp:
	f = json.load(fp)

names = set()
for species in f['species']:
	names.add(species['name'])

print('\n'.join(names))
