# Copyright (c) Peter Majko.

"""

"""

import pandas as pd


db = pd.read_excel('lm_db.xlsx', None)
equipment = db["lm_equipment"]
my_equipment = db["my_equipment"]
my_equipped_jewels = db["my_equipped_jewels"]
my_unequipped_jewels = db["my_unequipped_jewels"]

df = my_equipped_jewels.groupby(["name", "quality"]).size()
df = df.to_frame("quantity").reset_index()
df["const"] = 4
df["quantity"] = df.const.pow(df.quality - 1) * df.quantity
df = df[["name", "quality", "quantity"]].groupby("name").sum().reset_index()
df["quality"] = 1

df2 = my_unequipped_jewels[["name", "quality", "quantity"]]
df2["const"] = 4
df2["quantity"] = df2.const.pow(df2.quality - 1) * df2.quantity
df2 = df2[["name", "quality", "quantity"]].groupby("name").sum().reset_index()
df2["quality"] = 1

all_jewels = pd.concat(
    [df, df2], ignore_index=True
)[["name", "quantity"]].groupby("name").sum().reset_index().rename(
    columns={"name": "name", "quantity": "quantity_Q1"}
).sort_values("quantity_Q1", ascending=False)
all_jewels["max_quantity_Q2"] = all_jewels["quantity_Q1"] // 4
all_jewels["max_quantity_Q3"] = all_jewels["max_quantity_Q2"] // 4
all_jewels["max_quantity_Q4"] = all_jewels["max_quantity_Q3"] // 4
all_jewels["max_quantity_Q5"] = all_jewels["max_quantity_Q4"] // 4

print(all_jewels)


