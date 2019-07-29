# Copyright (c) Peter Majko.

"""

"""
import pandas as pd

DEFAULT_WEIGHTS_AIRC = {
    "arm": 3.0,
    "inf": 1.0,
    "rng": 1.0,
    "cav": 1.0
}

DEFAULT_WEIGHTS_AMD = {
    "atk": 0.5,
    "mhp": 0.2,
    "def": 0.1
}

DEFAULT_WEIGHTS = {
    f"{airc_key}_{amd_key}": airc_val * amd_val
    for airc_key, airc_val in DEFAULT_WEIGHTS_AIRC.items()
    for amd_key, amd_val in DEFAULT_WEIGHTS_AMD.items()
}

QUALITIES = (
    'Common',
    'Uncommon',
    'Rare',
    'Epic',
    'Legendary',
    'Mythic'
)

SLOTS = (
    "main_hand",
    "helmet",
    "armor",
    "legs",
    "off-hand",
    "accessory"
)

TROOPS = (
    "inf",
    "rng",
    "cav"
)

UNITS = (
    "Ancient Drake Rider",
    "Archer",
    "Cataphract",
    "Catapult",
    "Destroyer",
    "Fire Trebuchet",
    "Gladiator",
    "Grunt",
    "Heroic Cannoneer",
    "Heroic Fighter",
    "Reptilian Rider",
    "Royal Cavalry",
    "Royal Guard",
    "Sharpshooter",
    "Stealth Sniper"
)

LINEUPS = {
    "inf_phx": ()
}

EQUIPMENT_DB_DF = pd.read_excel('lm_db.xlsx', None)["lm_equipment"].fillna(0)
