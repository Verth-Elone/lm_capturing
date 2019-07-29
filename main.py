# Copyright (c) Peter Majko.

"""

"""
from app.models import Cabinet
import pandas as pd

if __name__ == '__main__':
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.expand_frame_repr', False)

    c = Cabinet()
    c.equipment.load_from_xlsx('lm_db.xlsx', 'my_equipment')
    e = c.equipment

    print(e.army_relevant)
    print(e.weighted_army_relevant)
    print(e.war_best)
    print(e.war_stats)
    print(e.war_stats.sum(axis=0))
