#!/usr/bin/env python
import context
import nbateammatechain.players.build_teammates as build_teammates
import nbateammatechain.utils.serialize as serialize
import shutil

player_dict = build_teammates.full_teammates()
serialize.create_pickle("player_dict_full.pickle", player_dict)
shutil.move("player_dict_full.pickle", "../raw_files/")
