from ..utils import soup_opt as soup
import re

class Player(object):
    """
    Creates a Player object, representing a particular player in the data 
    structure
    """
    # slots declared to increase efficiency
    __slots__ = ['name', 'height', 'weight', 'year', 'career_stats',
    'achievements', 'teammates']

    def __init__(self, name, height, weight, year, career_stats, achievements):
        # declare all fields in constructor to ensure serialization
        self.name = name # string
        self.height = height # int
        self.weight = weight # int
        self.year = year # int
        self.career_stats = career_stats # dict
        self.achievements = achievements # dict
        self.teammates = {} # dict

    def update_teammates(self, key, value):
        """
        Update dictionary of teammates
        """
        self.teammates[key] = value

def _convert_height(height):
    """
    This converts the height text found in bbref to an integer in inches
    """
    return int(height[0])*12+int(height[2:]) 

def parse_achievement(achievement):
    """
    Parses an achievement string to extract desired data in a key, value
    form
    """
    VALID_ACHIEVEMENT= ["All Star", "All Defensive", "NBA Champ", "All NBA"]

    # achievement string format example: "3x All-Defensive"
    # use regex instead of join to account for a hyphenated string    
    string = re.split('\W+', achievement)  # string is now a list of words
    # get key 
    # this is a string such as "NBA champ" or "All Defensive"
    key = " ".join(string[1:3])
    
    # find if achievement is a subset of what we care about
    isValid = False
    for element in VALID_ACHIEVEMENT:
        if key == element:
            isValid = True
    
    if not isValid:
        return None, None
    else:
        value = int(string[0][:-1])
        return key, value

def create_player(URL):
    """
    Parses and Analyzes player information to acquire stats and relevant 
    data to create player object, which it returns.
    """
    pl = soup.soup_streamline(URL) # all player URL procured data
    if pl is None:
        print URL + " is None"
        return None
    namestr = str(pl.find("h1").string)
    # returns name of player, exclude unwanted strings
    name = " ".join('{}'.format(i) for i in namestr.split(' ') if i!="Career" and i!="Splits")

    height = _convert_height(pl.find(itemprop="height").string)
    weight = int(pl.find(itemprop="weight").string[:3])

    for p in pl.find_all('p'):
        if 'Draft' in p.getText():
            for a in p.find_all('a'):
                if a.string[-9:] == 'NBA Draft':
                    global year
                    year = int(a.string[:4])+1

    # career stats maps out to 
    # GP, GS, MP, FG, FGA, 3P, 3PA, FT, FTA, TRB, AST, STL, BLK, PTS
    # FG%, 3P%, FT%, mpg, ppg, rpg, apg
    
    career_stats = {}
    # find siblings in parse tree to start from
    start = pl.find(attrs={'data-stat':'split_value'}, string="Total")
    float_breakpoint = False # initially set the value of a key to int
    for sibling in start.next_siblings:
        # key corresponds to the name of a particular stat
        # value is its value in integer or float form
        key = str(sibling['data-stat'])
        # all stats after float_breakpoint are stored in float form
        if key == "fg_pct":
            float_breakpoint = True
        # filter keys we don't care for
        filter_basic = key!='orb' and key!='tov' and key!="pf" 
        filter_adv_pct = key!='ts_pct' and key!='usg_pct'
        filter_adv_rtg = key!='off_rtg' and key!='def_rtg'
        if filter_basic and filter_adv_pct and filter_adv_rtg:
            # if the stat exists
            if sibling.string is not None:
                if float_breakpoint:
                    value = float(sibling.string)
                else:
                    value = int(sibling.string)
            else:
                value = 0
            # update career_stats dictionary
            career_stats[key] = value

    # achievements that include a large subset of players that we care about
    # All-star, Championships, All-NBA, All-Defensive
    
    achievements = {}
    # find children in parse tree to start from
    start = pl.find(id="bling")
    if start is not None:
        for child in start.children:
            # parse into usable values
            # key should be name of achievement
            # value should be the amount of times awarded
            key, value = parse_achievement(child.string)
            # if Nonetype not returned, add award to player achievenment
            # dictionary
            if key is not None:   
                achievements[key] = value

    #return player object
    return Player(name, height, weight, year, career_stats, achievements)
