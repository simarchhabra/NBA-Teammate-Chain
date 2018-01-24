#!/usr/bin/env python
import context
from nbateammatechain.utils import serialize
import shutil

player_dict = serialize.load_pickle('../raw_files/player_dict_full.pickle')

player_name_dict = {}
for player in player_dict:
    pl_list = player_name_dict.get(player)
    key = player_dict[player].name.lower()
    if pl_list is None:
        value = [player]
        player_name_dict[key] = value
    else:
        pl_list.append(player)
        assert player in player_name_dict[key]
filename = "player_name_dict.pickle"
serialize.create_pickle(filename, player_name_dict)
shutil.move(filename, "../raw_files/")


