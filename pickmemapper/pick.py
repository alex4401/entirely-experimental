# pick.py MODID MODNAMEIFMOD SPECIESNAME

import re
import sys
from pathlib import Path

src_path = Path('sources')
dst_path = Path('target')

modid = sys.argv[1]
modname = sys.argv[2]
species_name = sys.argv[3]

print(f'Resolving mod {modid}')
modid = modid.strip()
is_core = modid.lower() == 'core'
if not is_core:
	mod_matches = src_path.glob(f'*{modid}*')
	mod_path = list(mod_matches)[0]
else:
	mod_path = src_path

print(f'Picking {species_name} from {modid}')
species_name_c = species_name.replace(' ', '_')
if is_core:
	files = mod_path.glob(f'*/spawn_maps/Spawning_{species_name_c}.svg')
else:
	files = mod_path.glob(f'**/spawn_maps/**/Spawning_{species_name_c}.svg')

print(f'Copying picked files')
manifest = []
for file in files:
	input = file.read_text()
	if is_core:
		map_name = file.parents[1].name
	else:
		map_name = file.parent.name
	if map_name == 'TheIslandSubMaps':
		map_name = 'TheIsland'
	map_name = re.sub(r'\B([A-Z])', r' \1', map_name)
	if is_core:
		new_path = dst_path / f'Spawning {species_name} {map_name}.svg'
	else:
		if map_name == 'spawn_maps':
			map_name = modname
		new_path = dst_path / f'Mod {modname} Spawning {species_name} {map_name}.svg'

	print(f'\tCopying spawn map for {map_name}')
	manifest.append(str(new_path.name))
	new_path.write_text(input)

print(f'Generating the blacklist')
with open(dst_path / 'blacklist.txt', 'a') as fp:
	for file in manifest:
		fp.write(f'* [[:File:{file}]]\n')
