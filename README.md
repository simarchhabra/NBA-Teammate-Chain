# NBATeammateChain

This program creates a teammate chain from one player to another!
You can specify one attribute to maximize and the program will find the 
teammate with the highest value of that attribute. It will continue to do that
until a chosen player is reached. If there are equal teammates with that value,
the shorter path is chosen. You can also select no attribute and the shortest
path of teammates will be created!

## Requirements

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) >= 4.0

### Notes

Player data is only available for players drafted 1984 or after due to
restrictions with acquiring basketball-reference data. You can either use the
already acquired player data as of January 2018 or update the data yourself. To
acquire data, this program parses information from basketball-reference.com and
takes around 2 hours to run. There will be an option for acquiring data in the
main script.

#### Example Usage

To run the program, simply execute the main.py script

```
python main.py
```
To understand the program, the following is a sample example to find the path 
between Michael Jordan and Kobe Bryant (a path is a teammate chain) 
maximizing all star selections.

Michael Jordan (All Star Selections: 14) -->
Scottie Pippen (All Star Selections: 7) - Team(s) played together on:  ['CHI', '1988-1998'] -->
Hakeem Olajuwon (All Star Selections: 12) - Team(s) played together on: ['HOU', '1999-1999'] -->
Charles Barkley (All Star Selections: 11) - Team(s) played together on: ['HOU', '1997-2000'] -->
Clyde Drexler (All Star Selections: 10) - Team(s) played together on:  ['HOU', '1997-1998'] -->
Terry Porter (All Star Selections: 2) - Team(s) played together on:  ['POR', '1986-1995'] -->
Kevin Garnett (All Star Selections: 15) - Team(s) played together on:  ['MIN', '1996-1998'] -->
Shaquille O'Neal (All Star Selections: 15) - Team(s) played together on:  ['BOS', '2011-2011'] -->
Kobe Bryant (All Star Selections: 18) - Team(s) played together on:  ['LAL', '1997-2004']

The attribute maximized here is All Star Appearances!

Michael Jordan's teammate who received the largest number of all star selections
is Scottie Pippen at 7.

Pippen's teammate who has not already been listed who received the largest
number of selections is Hakeem Olajuwon at 12.

This continues until Kobe Bryant is reached. Note that this is the shortest
path from Jordan to Kobe, as other teammates may have equivalent number of
selections but result in a longer path.

##### Extra Information about the program

The following is the key for attributes tested:

DESCRIPTION                                     KEY

-----------                                     ---

Height                                          height

Weight                                          weight

Games Played                                    g

Games Started                                   gs

Career Minutes                                  mp

Career Points                                   pts

Career Assists                                  ast

Career Rebounds                                 trb

Career Steals                                   stl

Career Blocks                                   blk

Career Field Goals Attempted                    fga

Career Three Point Field Goals Attempted        fg3a

Career Free Throws Attempted                    fta

Career Field Goals Made                         fg

Career Three Point Field Goals Made             fg3

Career Free Throws Made                         ft

Career Field Goal Percentage                    fg_pct

Career Three Point Field Goal Percentage        fg3_pct

Career Free Throw Percentage                    ft_pct

Career Minutes Per Game                         mp_per_g

Career Points Per Game                          pts_per_g

Career Assist Per Game                          ast_per_g

Career Rebounds Per Game                        trb_per_g

Career Steals Per Game                          stl_per_g

Career Blocks Per Game                          blk_per_g

All Defensive Selections                        All Defensive

All NBA Selections                              All NBA

All Star Selections                             All Star

NBA Championships Won                           NBA Champ

Operations with attributes that may result in a heavy number of people having
that attribute value (such as height), a user may need to manually increase the 
max recursive depth that python allows.
