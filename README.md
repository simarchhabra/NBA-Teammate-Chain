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
Height

Weight

Games Played

Games Started

Career Minutes

Career Points

Career Assists

Career Rebounds

Career Steals

Career Blocks

Career Field Goals Attempted

Career Three Point Field Goals Attempted

Career Free Throws Attempted

Career Field Goals Made

Career Three Point Field Goals Made

Career Free Throws Made

Career Field Goal Percentage

Career Three Point Field Goal Percentage

Career Free Throw Percentage

Career Minutes Per Game

Career Points Per Game

Career Assist Per Game

Career Rebounds Per Game

Career Steals Per Game

Career Blocks Per Game

All Defensive Selections

All NBA Selections

All Star Selections

NBA Championships Won

Operations with attributes that may result in a heavy number of people having
that attribute value (such as height), a user may need to manually increase the 
max recursive depth that python allows.
