#!/usr/bin/env python
import context
import nbateammatechain.players.build_players as build_players
import nbateammatechain.utils.serialize as serialize
import shutil

player_dict = build_players.create_player_dict()
serialize.create_pickle("player_dict.pickle", player_dict)
shutil.move("player_dict.pickle", "../raw_files/")
