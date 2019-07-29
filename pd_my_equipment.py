# Copyright (c) Peter Majko.

"""

"""
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)

_WEIGHTS_AIRC = {
    "arm": 3.0,
    "inf": 1.0,
    "rng": 1.0,
    "cav": 1.0
}

_WEIGHTS_AMD = {
    "atk": 0.5,
    "mhp": 0.2,
    "def": 0.1
}

WEIGHTS = {}
for airc_key, airc_val in _WEIGHTS_AIRC.items():
    for amd_key, amd_val in _WEIGHTS_AMD.items():
        WEIGHTS[f"{airc_key}_{amd_key}"] = airc_val * amd_val

print(WEIGHTS, "\n")


EQUIP_SLOTS = [
    "main_hand",
    "helmet",
    "armor",
    "legs",
    "off-hand",
    "accessory",
    "accessory",
    "accessory"
]


db = pd.read_excel('lm_db.xlsx', None)
equipment = db["lm_equipment"].fillna(0)
my_equipment = db["my_equipment"]
# my_equipment = db["lm_equipment"].fillna(0)[['name', 'quality']]
# my_equipment = my_equipment[
#     my_equipment.name.str.contains('Champion') == False
# ]

# print(equipment.head())
# print(my_equipment.head())

# 1. get my items with stats
my_eqp_enh = my_equipment.merge(
    equipment, left_on=["name", "quality"], right_on=["name", "quality"]
)
sub = my_eqp_enh[["id", "name", "slot", "quality"] + [key for key in WEIGHTS.keys()]]
sub = sub.reset_index(drop=True)
sub["weight"] = 0.0
for column in sub.columns:
    if column in WEIGHTS:
        sub["weight"] += (sub[column] * WEIGHTS[column])
sub = sub.sort_values("weight", ascending=False).reset_index(drop=True)

df = sub

df['rank'] = df.groupby(by=['slot'])['weight'].transform(
    lambda x: x.rank(method='min', ascending=False)
)

slot_dfs = []
for slot in df.slot.unique():
    df_slot = df[(df['slot'] == slot)]
    if slot == 'accessory':
        df_slot = df_slot.head(3)
    else:
        df_slot = df_slot[df_slot['rank'] == 1].head(1)
    slot_dfs.append(df_slot)

df = pd.concat(slot_dfs)
print(df)
print(df.sum(axis=0))


