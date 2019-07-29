# Copyright (c) Peter Majko.

"""

"""

import pandas as pd


db = pd.read_excel('lm_db.xlsx', None)
equipment = db["lm_equipment"]
df = equipment.fillna(0)

print(df['name'][df['arm_atk'].idxmax()])

print(df.slot.unique())

stat = 'arm_atk'
sum_max = 0
for slot in df.slot.unique():
    subset = df.where(df.slot == slot)
    id_max = subset[stat].idxmax()
    val_max = subset[stat][id_max]
    item_max = subset.name[id_max]
    sum_max += val_max
    print(slot, item_max, val_max)

print(sum_max)
