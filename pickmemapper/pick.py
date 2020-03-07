# pick.py ASBID DINONAMES...

import json
import re
import sys
from pathlib import Path

HEAD_SIZE = 32

src_path = Path('sources')
dst_path = Path('target')

asb_id = sys.argv[1]
species_names = sys.argv[2:]

def _resolve_files(path, pattern):
	files = path.glob(pattern)
	return list(files)

def _load_json(path):
	with open(path, 'r') as fp:
		return json.load(fp)

print('Resolving ASB data')
asb_file = _resolve_files(src_path, f'*{asb_id}*.json')[0]
asb = _load_json(asb_file)

if 'mod' in asb:
	print('NOT IMPLEMENTED YET')
else:
	modid = 0
	modname = 'core'

print('Resolving extended mod data')
if modid:
	base_path = src_path.glob(f'*{modid}*')[0]
else:
	base_path = src_path


print()
print('Mod details')
print('=' * HEAD_SIZE)
print(f'ID\t\t: {modid if modid else "N/A"}')
print(f'Name\t\t: {modname}')
print(f'Data\t\t: {base_path}')
print(f'# of Dinos\t: {len(asb["species"])}')
print('=' * HEAD_SIZE)
print()

def _resolve_dino(asb, name):
	v0 = list()
	v1 = list()
	for species in asb['species']:
		if name == species['name']:
			v0.append(species)
		elif name in species['blueprintPath'].rsplit('.', 1)[1]:
			v1.append(species)
	return [*v0, *v1]

def make_x_class(x):
	dino_class = x['blueprintPath']
	dino_class_short = dino_class.rsplit('.', 1)[1]
	x['x-class'] = dino_class_short
	return dino_class_short

def _choose_dino(classes):
	if len(classes) <= 1:
		return classes
	print('\t\tChoose:')
	for id, x in enumerate(classes):
		dino_class_short = make_x_class(x)
		print(f'\t\t[{id}] {x["name"]} ({dino_class_short})')

	data = input('\t\t[?] ')
	if data == '*':
		return classes
	return [classes[int(choice.strip())] for choice in data.split(',')]

dino_classes = list()
print('Resolving dinos')
pad = max(len(x) for x in species_names)
for dino_name in species_names:
	if dino_name.startswith('p='):
		pattern = dino_name[2:]
		print(f'\tMatching pattern: {pattern}')
		pattern = re.compile(pattern)
		for dino in asb['species']:
			if pattern.match(dino['blueprintPath']):
				make_x_class(dino)
				print(f'\t\t+ {dino["x-class"]}')
				dino_classes.append(dino)
	else:
		print(f'\t{dino_name.ljust(pad)}: ', end='')
		matches = _resolve_dino(asb, dino_name)
		print(f'{len(matches)} match(es)')
		dino_classes += _choose_dino(matches)
print(f'{len(dino_classes)} classes have been chosen.')

print(f'Picking spawning maps for chosen dino classes')
pad = max(len(x['x-class']) for x in dino_classes)
files = list()
for id, dino in enumerate(dino_classes):
	dino_class = dino['x-class']
	print(f'\t[{id}] {dino_class.ljust(pad)}: ', end='')
	if modid:
		dino_files = base_path.glob(f'**/spawn_maps/**/Spawning_{dino_class}.svg')
	else:
		dino_files = base_path.glob(f'*/spawn_maps/Spawning_{dino_class}.svg')
	dino_files = list(dino_files)
	print(f'{len(dino_files)} match(es)')
	files += ((dino, dino_files), )

print()
print('Review')
print('=' * HEAD_SIZE)
print(f'Mod\t\t: {modid}-{modname}')
print(f'Data\t\t: {base_path}')
#print(f'# of Files\t: {len(x[2]) for x in files}')
print('=' * HEAD_SIZE)
print()

print('Proceed? [y/n] ', end='')
if input().lower().strip() != 'y':
	sys.exit(0)

print(f'Copying picked files')
manifest = []
for descriptor in files:
	species_name = descriptor[0]['name']

	if 'variants' in descriptor[0]:
		for variant in descriptor[0]['variants']:
			species_name = f'{variant} {species_name}'

	for file in descriptor[1]:
		input = file.read_text()

		if modid:
			map_name = file.parent.name
		else:
			map_name = file.parents[1].name
		map_name = re.sub(r'\B([A-Z])', r' \1', map_name)

		if modid:
			if map_name == 'spawn_maps':
				map_name = modname
			new_path = dst_path / f'Mod {modname} Spawning {species_name} {map_name}.svg'
		else:
			new_path = dst_path / f'Spawning {species_name} {map_name}.svg'

		print(f'\tCopying spawn map of {species_name} on {map_name}')
		file_name = str(new_path.name)

		if file_name in manifest:
			print(f'\t\tCollision!')

		manifest.append(file_name)
		new_path.write_text(input)

print(f'Generating the blacklist')
manifest.sort()
with open(dst_path / 'blacklist.txt', 'a') as fp:
	for file in manifest:
		fp.write(f'* [[:File:{file}]]\n')
