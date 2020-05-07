# Common
IgnoreClasses_ModGlobal = {
    'Gacha_Claus_Character_BP',
    'Dodo_Character_BP_Bunny',
}
def _flt_skip_existing_variant(a, b) -> bool:
    return b not in a

# Primal Fear
Mod_839162288 = {
    'Origin Carno': 'Origin Carnotaurus',
    'Apex Dilophosaurus': 'Apex Dilophosaur',
    'Alpha Dilophosaurus': 'Alpha Dilophosaur',
}
IgnoreClasses_839162288 = IgnoreClasses_ModGlobal
Variants_839162288 = False

# Primal Fear Bosses
IgnoreClasses_899987403 = IgnoreClasses_ModGlobal
Variants_899987403 = False

# Primal Fear Extinction
# CAN BE SKIPPED
IgnoreClasses_1681125667 = IgnoreClasses_ModGlobal
Variants_1681125667 = False

# Primal Fear Noxious
IgnoreClasses_1356703358 = IgnoreClasses_ModGlobal
Variants_1356703358 = False

# Ark Eternal
ModName_893735676 = 'Ark Eternal'
Mod_893735676 = {
    'Rock Elemental': 'Bacon Overlord',
}
IgnoreClasses_893735676 = {*IgnoreClasses_ModGlobal, *{
    'Otter_Character_BP_AE',
    'Mantis_Character_BP_Child',
    'Arthro_Character_BP_Corrupt',
    'Carno_Character_BP_Corrupt',
    'Chalico_Character_BP_Corrupt',
    'Dilo_Character_BP_Corrupt',
    'Dimorph_Character_BP_Corrupt',
    'Gigant_Character_BP_Corrupt',
    'Paracer_Character_BP_Corrupt',
    'Ptero_Character_BP_Corrupt',
    'Raptor_Character_BP_Corrupt',
    'Xenomorph_Character_BP_Male_Tamed_Corrupt',
    'Rex_Character_BP_Corrupt',
    'RockDrake_Character_BP_Corrupt',
    'Spino_Character_BP_Corrupt',
    'Stego_Character_BP_Corrupt',
    'Trike_Character_BP_Corrupt',
    'Wyvern_Character_BP_Fire_Corrupt',
    'Griffin_Character_BP_AE',
}}
Variants_893735676 = False

# Core
Maps = {
    'The Island Sub Maps': 'The Island',
    'Genesis': 'Genesis Part 1',
}

VariantFilter = _flt_skip_existing_variant
