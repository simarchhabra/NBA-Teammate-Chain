#!/usr/bin/env python
from __future__ import print_function

import os
os.system('clear')

print("\n\nDESCRIPTION: This program creates a teammate chain from one player to another!")
print("\n\nDETAILS: You can specify one attribute to maximize and the program will find" + 
        " the teammate with the highest value of that attribute.\nIt will" +
        " continue to do that until a chosen player is reached. If there are" +
        " equal teammates with that value, the shorter path is chosen.\nYou" +
        " can also select no attribute and the shortest path of teammates " +
        " will be created!")
print("\n\nEXAMPLE: If you want to find the chain of teammates from Michael" +
        " Jordan and Kobe Bryant maximizing all star selections, you get " +
        "a resultant path of\nMichael Jordan (All Star Selections: 14) -->\n" +
        "Scottie Pippen (All Star Selections: 7) - Team(s) played together on:  ['CHI', '1988-1998'] -->\n" +
        "Hakeem Olajuwon (All Star Selections: 12) - Team(s) played together on:  ['HOU', '1999-1999'] -->\n" +
        "Charles Barkley (All Star Selections: 11) - Team(s) played together on:  ['HOU', '1997-2000'] -->\n" +
        "Clyde Drexler (All Star Selections: 10) - Team(s) played together on:  ['HOU', '1997-1998'] -->\n" +
        "Terry Porter (All Star Selections: 2) - Team(s) played together on:  ['POR', '1986-1995'] -->\n" +
        "Kevin Garnett (All Star Selections: 15) - Team(s) played together on:  ['MIN', '1996-1998'] -->\n" +
        "Shaquille O'Neal (All Star Selections: 15) - Team(s) played together on:  ['BOS', '2011-2011'] -->\n" +
        "Kobe Bryant (All Star Selections: 18) - Team(s) played together on:  ['LAL', '1997-2004']\n")

print("\n\nEXPLANATION: The attribute maximized here is All Star Appearances!" + 
        "\nMichael Jordan's teammate who received the largest number of all " +
        "star selections is Scottie Pippen at 7.\nPippen's teammate who has" +
        " not already been listed who received the largest number of " +
        "selections is Hakeem Olajuwon at 12.\nThis continues until Kobe " +
        "Bryant is reached. Note that this is the shortest path from Jordan" +
        " to Kobe, as other teammates may have equivalent number of " +
        "selections but result in a longer path.")

print("\n\nPlayer data is only available for players drafted 1984 or after due" +
        " to restrictions with acquiring basketball-reference data. You can "
        + "either use the already acquired player data as of January 2018 or" +
        " update the data yourself. To acquire data, this program parses " +
        "information from basketball-reference.com and takes around 2 hours to"
        " run.")

player_update_str = raw_input("\nUpdate player data [Y/N]? ").lower()
player_update = False
if player_update_str[0] == 'y':
    player_update = True
elif player_update_str[0] == 'n':
    pass
else:
    print("Default for no [y/n] is no. No player data update.")

import nbateammatechain.utils.serialize as serialize

if player_update:
    print("To quit update, press Ctrl-C. You may need to press a few times.")
    import os
    import nbateammatechain.players.build_teammates as build_teammates
    import shutil

    player_dict = build_teammates.full_teammates()
    filename = "player_dict_full.pickle"
    try:
        os.remove(filename)
    except OSError:
        pass
    serialize.create_pickle(filename, player_dict)
    shutil.move(filename, "/raw_files/")

print("\n\nLoading Player Data and Building Graph Connections...")
import nbateammatechain.graph.player_graph as graph
player_name_dict = serialize.load_pickle("raw_files/player_name_dict.pickle")
player_dict = serialize.load_pickle("raw_files/player_dict_full.pickle")
Graph = graph.Graph()

attr_key = [('Height', 'height'), ('Weight', 'weight'), ('Games Played',
    'g'), ('Games Started', 'gs'), ('Career Minutes', 'mp'), 
    ('Career Points', 'pts'), ('Career Assists', 'ast'), 
    ('Career Rebounds', 'trb'), ('Career Steals', 'stl'), ('Career Blocks', 
    'blk'), ('Career Field Goals Attempted', 'fga'), 
    ('Career Three Point Field Goals Attempted', 'fg3a'),
    ('Career Free Throws Attempted', 'fta'),
    ('Career Field Goals Made', 'fg'),
    ('Career Three Point Field Goals Made', 'fg3'),
    ('Career Free Throws Made', 'ft'), ('Career Field Goal Percentage', 
    'fg_pct'), ('Career Three Point Field Goal Percentage', 'fg3_pct'), 
    ('Career Free Throw Percentage', 'ft_pct'), ('Career Minutes Per Game',
    'mp_per_g'), ('Career Points Per Game','pts_per_g'), 
    ('Career Assist Per Game', 'ast_per_g'), ('Career Rebounds Per Game', 
    'trb_per_g'), ('Career Steals Per Game', 'stl_per_g'), 
    ('Career Blocks Per Game', 'blk_per_g'), ('All Defensive Selections', 
    'All Defensive'), ('All NBA Selections', 'All NBA'), 
    ('All Star Selections', 'All Star'), ('NBA Championships Won', 
    'NBA Champ')]
    
print("\n\n\n\nThe following key represents attributes you can test for.")
print("If you want no attribute tested for, press enter or type any other string.")
print("\nKey for attribute testing:")
print("DESCRIPTION                                     KEY")
print("-----------                                     ---")
for description, key in attr_key:
    print("{:<48}{}".format(description, key))

print("\nNote for operations with attributes that may result in a heavy number"
        + " of people having that attribute value (such as height), you may have to" 
        + " manually increase max recursive depth that python allows.")

paths = []
while True:
   
    l = []
    key = raw_input("\n\nKey: ")
    l = filter(lambda x: x[1] == key, attr_key)
    attr = None
    
    if len(l) == 0:
        pass
    else:
        attr = l[0][1]
    
    stored_attr = attr
    
    dict_key = None
    if attr == 'height' or attr == 'weight':
        pass
    elif attr == 'All Defensive' or attr == 'All NBA' or attr == 'All Star' or attr == 'NBA Champ':
        dict_key = 'achievements'
        attr, dict_key = dict_key, attr
    elif(attr == 'g' or attr == 'gs' or attr == 'mp' or attr == 'pts' or 
            attr == 'ast' or attr == 'trb' or attr == 'stl' or attr == 'blk' or
            attr == 'fga' or attr == 'fg3a' or attr == 'fta' or attr == 'fg' or
            attr == 'fg3' or attr == 'ft' or attr == 'fg_pct' or 
            attr == 'fg3_pct' or attr == 'ft_pct' or attr == 'mp_per_g' or 
            attr == "pts_per_g" or attr == "ast_per_g" or attr == "trb_per_g" or
            attr == "stl_per_g" or attr == "blk_per_g"):
        dict_key = 'career_stats'
        attr, dict_key = dict_key, attr
    else:
        pass

    players_defined = False
    while not players_defined:
        
        print("\n\nFind path from Player 1 to Player 2. Make sure to enter their full names.")
        p1_name = raw_input("\nPlayer 1 Name: ").lower()
        p2_name = raw_input("Player 2 Name: ").lower()
        p1_id = None
        p2_id = None
        
        try:
            p1_id = player_name_dict[p1_name]
        except KeyError:
            print("\nERROR: Player just entered is not defined in Player's list.")
            print("Note: Remember players drafted before 1984 not defined.\n\n")
            continue
        try:
            p2_id = player_name_dict[p2_name]
        except KeyError:
            print("\nERROR: Player just entered is not defined in Player's list.")
            print("Note: Remember players drafted before 1984 not defined\n\n")
            continue
        
        players_defined = True
    Graph.update_attr(attr, dict_key)
    paths.append(Graph.build_path(p1_id[0], p2_id[0]))
     
    print(end="\n\n")
        
    last_teammate_list = list()
    if paths[-1] is None:
        print("No path found.")
    else:
        for i in range(len(paths[-1])):
            
            p_id = None
            if attr is not None:
                p_id = paths[-1][i][0]
            else:
                p_id = paths[-1][i]
            
            pl = player_dict[p_id]
            p_name = pl.name
            
            if i != len(paths[-1])-1:

                t_id = None
                if attr is not None:
                    t_id = paths[-1][i+1][0]
                else:
                    t_id = paths[-1][i+1]
                
                team_list = pl.teammates[t_id]
                team_values = []
                last_team = None
                
                for j in range(len(team_list)):
                    if team_list[j][0] != last_team:
                        last_team = team_list[j][0]
                        team_values.append([team_list[j][0], team_list[j][1]])
                    else:
                        try:
                            team_values[-1][2] = team_list[j][1]
                        except IndexError:
                            team_values[-1].append(team_list[j][1])

                for element in team_values:
                    if len(element) == 2:
                        element.append(element[1])
                    element[1] = str(element[1]) + "-" + str(element[2])
                    del element[2]
                    element = tuple(element)
            
            if attr is not None:
                attr_str = None
                for element in attr_key:
                    if element[1] == stored_attr:
                        attr_str = element[0]
                        break
                
                if i == 0:
                    print(p_name, "(" + attr_str + ": " + str(paths[-1][i][1]) + ") ",
                            end="-->\n")
                elif i != len(paths[0])-1:
                    print(p_name, "(" + attr_str + ": " + str(paths[-1][i][1]) + ")"
                            + " - Team(s) played together on: ", *last_teammate_list,
                            end=" -->\n")
                else:
                    print(p_name, "(" + attr_str + ": " + str(paths[-1][i][1]) + ")"
                            + " - Team(s) played together on: ",
                            *last_teammate_list)

            else:
                if i == 0:
                    print(p_name, end =" -->\n")
                elif i != len(paths[0])-1:
                    print(p_name + " - Team(s) played together on: ",
                            *last_teammate_list, end=" -->\n")
                else:
                    print(p_name + " - Team(s) played together on: ",
                            *last_teammate_list)

            last_teammate_list = team_values 
    
    quit = raw_input("\n\nDo you want to quit? [Y/N]").lower()
    if quit[0] == 'y':
        break 
