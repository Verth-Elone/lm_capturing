# Copyright (c) Peter Majko.

"""

"""
import pandas as pd

from .defaults import (
    DEFAULT_WEIGHTS, QUALITIES, SLOTS, EQUIPMENT_DB_DF
)


class Cabinet:

    def __init__(self):
        self.weights: dict = dict(DEFAULT_WEIGHTS)
        self.equipment: Equipment = Equipment(self)
        self.jewels: Jewels = Jewels()

    def restore_default_weights(self):
        self.weights = dict(DEFAULT_WEIGHTS)

    def restore_defaults(self):
        self.restore_default_weights()


class Equipment:
    """
    Properties:
        .all:      pandas.DataFrame with columns [id, name, quality],
                    containing all equipment owned by user enhanced with
                    equipment master data.
    """
    slots: tuple = SLOTS
    qualities: tuple = QUALITIES

    def __init__(self, cabinet):
        self.cabinet: Cabinet = cabinet
        self.all: pd.DataFrame = pd.DataFrame()

    def load_from_df(self, equipment_df: pd.DataFrame) -> None:
        """
        Loads enhanced equipment df into self.all; Refer to class docstring
         for more info.
        :param equipment_df: pandas.DataFrame with columns [id, name, quality]
        :return: None
        """
        df = equipment_df[['id', 'name', 'quality']]
        self.all = df.merge(
            EQUIPMENT_DB_DF, left_on=["name", "quality"],
            right_on=["name", "quality"]
        )

    @property
    def army_relevant(self):
        ar_df = self.all[
            ["id", "name", "slot", "quality"]
            + [key for key in self.cabinet.weights.keys()]
            ]
        ar_df = ar_df.reset_index(drop=True)
        ar_df['sum'] = sum([ar_df[c] for c in self.cabinet.weights.keys()])
        ar_df = ar_df[ar_df['sum'] > 0].drop(['sum'], axis=1)
        return ar_df

    @property
    def weighted_army_relevant(self):
        war_df = self.army_relevant
        war_df = war_df.reset_index(drop=True)
        war_df["weight"] = 0.0
        for column in war_df.columns:
            if column in self.cabinet.weights:
                war_df["weight"] += (
                        war_df[column] * self.cabinet.weights[column]
                )
        war_df = war_df.sort_values(
            "weight", ascending=False
        ).reset_index(drop=True)
        war_df['rank'] = war_df.groupby(by=['slot'])['weight'].transform(
            lambda x: x.rank(method='min', ascending=False)
        )
        return war_df

    @property
    def war(self):
        return self.weighted_army_relevant

    @property
    def war_best(self):
        df = self.war
        slot_dfs = []
        for slot in df.slot.unique():
            df_slot = df[(df['slot'] == slot)]
            if slot == 'accessory':
                df_slot = df_slot.head(3)
            else:
                df_slot = df_slot[df_slot["rank"] == 1.0].head(1)
            slot_dfs.append(df_slot)
        df = pd.concat(slot_dfs)
        return df

    @property
    def war_stats(self):
        stats = self.war_best[[key for key in self.cabinet.weights.keys()]]
        return stats.sum(axis=0)

    def load_from_xlsx(self, xlsx_path: str, sheet_name: str) -> None:
        self.load_from_df(pd.read_excel(io=xlsx_path, sheet_name=sheet_name))


class Jewels:

    qualities: tuple = QUALITIES[:-1]
