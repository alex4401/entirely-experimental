# pick.py ASBID DINONAMES...

import json
import re
import sys
from pathlib import Path

import nameoverrides

HEAD_SIZE = 32

src_path = Path('sources')
dst_path = Path('target')

asb_id = sys.argv[1]
species_names = sys.argv[2:]
filter(lambda x: x.startswith('-'), species_names)
CFG_SPEECHLESS = '-speechless' in sys.argv
CFG_CONFLICTS = '-conflicts' in sys.argv
CFG_DONTNOD = '-nonod' in sys.argv
CFG_VERBOSE = '-verbose' in sys.argv

def prints(*args, **kwargs):
    if not CFG_SPEECHLESS:
        print(*args, **kwargs)
        
        
def printd(*args, **kwargs):
    if CFG_VERBOSE:
        print(*args, **kwargs)


def end_if(condition):
    if condition:
        sys.exit(0)


def _resolve_files(path, pattern):
    files = path.glob(pattern)
    return list(files)


def _load_json(path):
    with open(path, 'r') as fp:
        return json.load(fp)


def trace(print_result=False, print_args=False, if_true=False):
    def __trace__(func):
        if not CFG_VERBOSE or f'-no-trace:{func.__name__}' in sys.argv:
            return func
    
        def __inner__(*args, **kwargs):
            result = func(*args, **kwargs)
            if if_true and not result:
                return result
        
            if print_result:
                print(f' [T] {func.__name__} ({len(args)} + {len(kwargs)}) -> {result}')
            else:
                print(f' [T] {func.__name__} ({len(args)} + {len(kwargs)})')
            
            if print_args:
                print(f'Args: {args}\nKwargs: {kwargs}\n====')
            
            return result
        return __inner__
    return __trace__


def _get_prop(name, core_name=None):
    if modid:
        first_name = f'{name}_{modid}'
    elif core_name:
        first_name = core_name
    else:
        first_name = name
        
    result = nameoverrides.__dict__.get(first_name, None)
    if result == None:
        result = nameoverrides.__dict__.get(name, None)
    return result
    

print('Resolving ASB data')
asb_file = _resolve_files(src_path, f'*{asb_id}*.json')[0]
asb = _load_json(asb_file)

if 'mod' in asb:
    modid = asb['mod']['id']
    modtag = asb['mod']['tag']
    modname = _get_prop('ModName') or asb['mod']['title']
else:
    modid = 0
    modtag = ''
    modname = 'core'
modname = modname.replace(':', '')

print('Resolving extended mod data')
#if modid:
#    base_path = list(src_path.glob(f'*{modid}*'))[0]
#else:
base_path = src_path
    

def _get_dino_name_override(input):
    ov = _get_prop('Mod', core_name='Core')
    if not ov:
        return input

    return ov.get(input, input)


@trace(print_result=True, if_true=True)
def _should_do_variants(input):
    ov = _get_prop('Variants')

    if isinstance(ov, bool):
        return ov

    if not ov:
        return True

    return ov.get(input, True)


def _should_add_variant(species_name, variant):
    flt = _get_prop('VariantFilter')
    if not flt:
        return True

    return flt(species_name, variant)

@trace(print_result=True, if_true=True)
def _should_ignore_dino(cls):
    ov = _get_prop('IgnoreClasses')
    if not ov:
        return False
    return cls['x-class'] in ov

print()
print('Mod details')
print('=' * HEAD_SIZE)
print(f'ID\t\t: {modid if modid else "N/A"}')
print(f'Tag\t\t: {modtag}')
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
    filter(lambda x: not _should_ignore_dino(x), classes)

    if len(classes) <= 1:
        make_x_class(classes[0])
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
        prints(f'\tMatching pattern: {pattern}')
        pattern = re.compile(pattern)
        for dino in asb['species']:
            if pattern.match(dino['blueprintPath']):
                make_x_class(dino)
                if _should_ignore_dino(dino):
                    continue
                
                prints(f'\t\t+ {dino["x-class"]}')
                dino_classes.append(dino)
    else:
        prints(f'\t{dino_name.ljust(pad)}: ', end='')
        matches = _resolve_dino(asb, dino_name)
        prints(f'{len(matches)} match(es)')
        dino_classes += _choose_dino(matches)
print(f'{len(dino_classes)} classes have been chosen.')

print(f'Picking spawning maps for chosen dino classes')
pad = max(len(x['x-class']) for x in dino_classes)
files = list()
for id, dino in enumerate(dino_classes):
    dino_class = dino['x-class']
    prints(f'\t[{id}] {dino_class.ljust(pad)}: ', end='')
    if modid:
        specific_path = f'{modid}-{modtag}/spawn_maps/**/Spawning_{dino_class}_({modid}).svg'
    else:
        specific_path = f'*/spawn_maps/Spawning_{dino_class}.svg'
    dino_files = list(base_path.glob(specific_path))
    prints(f'{len(dino_files)} match(es)')
    files += ((dino, dino_files), )
    

print()
print('Review')
print('=' * HEAD_SIZE)
print(f'Mod\t\t: {modid}-{modname}')
print(f'Data\t\t: {base_path}')
#print(f'# of Files\t: {len(x[2]) for x in files}')
print('=' * HEAD_SIZE)
print()

if not CFG_DONTNOD:
    print('Proceed? [y/n] ', end='')
    if input().lower().strip() != 'y':
        sys.exit(0)


def _format_map_name(file):
    if modid:
        map_name = file.parent.name
    else:
        map_name = file.parents[1].name
    map_name = re.sub(r'\B([A-Z])', r' \1', map_name)

    map_name = nameoverrides.Maps.get(map_name, map_name)
    return map_name


def _get_output_path(map_name, path):
    if modid:
        if map_name == 'spawn_maps':
            map_name = modname
        new_path = dst_path / f'Mod {modname} Spawning {species_name} {map_name}.svg'
    else:
        new_path = dst_path / f'Spawning {species_name} {map_name}.svg'
    return new_path


if CFG_CONFLICTS:
    print(f'Checking for conflicts')
else:
    print(f'Copying picked files')

manifest = []
manifest_dinos = []
for descriptor in files:
    species_name = descriptor[0]['name']

    if 'variants' in descriptor[0] and _should_do_variants(
            descriptor[0]['name']):
        for variant in descriptor[0]['variants']:
            if _should_add_variant(species_name, variant):
                species_name = f'{variant} {species_name}'

    species_name = _get_dino_name_override(species_name)

    for file in descriptor[1]:
        input = file.read_text()
        map_name = _format_map_name(file)
        new_path = _get_output_path(map_name, file)

        prints(f'\tCopying spawn map of {species_name} on {map_name}')
        file_name = str(new_path.name)

        if file_name in manifest:
            if CFG_CONFLICTS or CFG_SPEECHLESS:
                print(f'\t\tDetected collision: {species_name} ({descriptor[0]["x-class"]})')
            else:
                print(f'\t\tCollision!')

        manifest.append(file_name)
        if species_name not in manifest_dinos:
            manifest_dinos.append(species_name)
        if not CFG_CONFLICTS:
            new_path.write_text(input)
        
end_if(CFG_CONFLICTS)

print(f'Generating the species list')
manifest_dinos.sort()
with open(dst_path / 'species.txt', 'a') as fp:
    for species in manifest_dinos:
        fp.write(f'{species}\n')

print(f'Generating the blacklist')
manifest.sort()
with open(dst_path / 'blacklist.txt', 'a') as fp:
    for file in manifest:
        fp.write(f'* [[:File:{file}]]\n')
