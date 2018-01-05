from .. import soup_opt as soup
import re

class Player(object):
    # slots declared to increase efficiency
    __slots__ = ['_name', '_height', '_weight', '_career_stats', 
            '_achievements', '_teammates']

    def __init__(self, name, height, weight, career_stats, achievements):
        # declare all fields in constructor to ensure serialization
        self._name = name # string
        self._height = height # int
        self._weight = weight # int
        self._career_stats = career_stats # dict
        self._achievements = achievements # dict
        self._teammates = {} # dict

    def update_teammates(self, key, value):
        """
        Update dictionary of teammates
        """
        self._teammates[key] = value

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

    # use regex instead of join to account for a hyphenated string    
    string = re.split('\W+', achievement)  #string is now a list of words
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

def create_player(bbref_url):
    """
    Parses and Analyzes player information to acquire stats and relevant 
    data to create player object, which it returns.
    """
    bbref_pl = soup.soup_streamline(bbref_url)
    # all basketball-reference procured data
    
    namestr = str(bbref_pl.find("h1").string)
    # returns name of player, exclude unwanted strings
    name = " ".join('{}'.format(i) for i in namestr.split(' ') if i!="Career"
            and i!="Splits")

    height = _convert_height(str(bbref_pl.find(itemprop="height").string))
    weight = int(str(bbref_pl.find(itemprop="weight").string)[:3])
    
    # career stats maps out to 
    # GP, GS, MP, FG, FGA, 3P, 3PA, FT, FTA, TRB, AST, STL, BLK, PTS
    # FG%, 3P%, FT%, mpg, ppg, rpg, apg
    
    career_stats = {}
    # find siblings in parse tree to start from
    start = bbref_pl.find(attrs={'data-stat':'split_value'}, string="Total")
    float_breakpoint = False # initially set key to int
    for sibling in start.next_siblings:
        key = str(sibling['data-stat'])
        if key == "fg_pct":
            float_breakpoint = True
        filter_basic = key!='orb' and key!='tov' and key!="pf" 
        filter_adv_pct = key!='ts_pct' and key!='usg_pct'
        filter_adv_rtg = key!='off_rtg' and key!='def_rtg'
        if filter_basic and filter_adv_pct and filter_adv_rtg:
            if sibling.string is not None:
                if float_breakpoint:
                    value = float(str(sibling.string))
                else:
                    value = int(str(sibling.string))
            else:
                value = 0
            career_stats[key] = value

    # achievements that include a large subset of players that we care about
    # All-star, Championships, All-NBA, All-Defensive
    
    achievements = {}
    # find children in parse tree to start from
    start = bbref_pl.find(id="bling")
    if start is not None:
        for child in start.children:
            # parse into usable values
            key, value = parse_achievement(str(child.string))
            if key is not None:   
                achievements[key] = value

    return Player(name, height, weight, career_stats, achievements)

if __name__=='__main_':
    lebron = create_player("https://www.basketball-reference.com/players/j/jamesle01/splits/")
    print lebron._career_stats
