# Copyright (c) Peter Majko.

"""

"""


class Cabinet:
    
    def __init__(self, equipment: list = None, jewels: list = None):
        self.equipment: list = [] if not equipment else equipment
        self.jewels: list = [] if not jewels else jewels
