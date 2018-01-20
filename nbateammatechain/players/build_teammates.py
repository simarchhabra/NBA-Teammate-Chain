import player, build_players
import time
from ..utils import serialize, soup_opt, convert_date

# years we care about
B_YEAR = 1984
E_YEAR = 2018
# player_dict = serialize.load_pickle('../raw_files/player_dict.pickle')

# create player dictionary (w/o teammates)
player_dict = build_players.create_player_dict()
# base url for all soup objects
base_URL = "https://www.basketball-reference.com/teams/"
suffix = ".html"
# list of teams based on the year they existed
teams = ['ATL', 'BOS', ('NJN', B_YEAR, 2012), ('BRK', 2013, E_YEAR), ('CHH',
    1989, 2002), ('CHA', 2005, 2014), ('CHO', 2015, E_YEAR), 'CHI', 'CLE', 
    'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', ('SDC', 1984, 1984), 
    ('LAC', 1985, E_YEAR), 'LAL', ('VAN', 1996, 2001), ('MEM', 2002, E_YEAR), 
    ('MIA', 1989, E_YEAR), 'MIL', ('MIN', 1990, E_YEAR), ('NOH', 2003, 2005), 
    ('NOK', 2006, 2007), ('NOH', 2008, 2013), ('NOP', 2014, E_YEAR), 'NYK', 
    ('SEA', B_YEAR, 2008), ('OKC', 2009, E_YEAR), ('ORL', 1990, E_YEAR), 'PHI', 
    'PHO', 'POR', ('KCK', B_YEAR, 1985), ('SAC', 1986, E_YEAR), 'SAS', 
    ('TOR', 1996, E_YEAR), 'UTA', ('WSB', B_YEAR, 1997), ('WAS', 1998, E_YEAR)]

class Team(object):
    """
    Class to represent a team over the course of the year
    """
   
    # represent dates that the season begins and ends, respectively
    START_DATE = "October 15, "
    END_DATE = "April 15, "
    
    def __init__(self, team_name, year):

        """
        Initializes team information including name, year and roster
        """

        self.team_name = team_name
        self.year = year
        
        # store URL's of team clubhouse and transactions as soup objects
        URL = base_URL + str(team_name) + "/" + str(year) + suffix
        transactionsURL = base_URL + team_name + "/" + str(year) + "_transactions" + suffix
        
        team_page = soup_opt.soup_streamline(URL)
        time.sleep(0.15)
        team_transactions = soup_opt.soup_streamline(transactionsURL)
        time.sleep(0.1)


        # store season beginning and ending dates into custom format
        BEGIN = convert_date.conversion(Team.START_DATE+str(int(year)-1))
        END = convert_date.conversion(Team.END_DATE+str(int(year)))
        
        # store roster of all players who played for team in the season
        # key = player id
        # value  = list -> [player object, date entered team, date left
        # team that year]
        # init. dates to season beginning date, season ending date
        self.roster = {} 
        for data in team_page.tbody:
            parsed_data = data.find('td')
            if parsed_data != -1:
                if year != E_YEAR:
                    pl_id = parsed_data['data-append-csv']
                    if player_dict.has_key(pl_id):
                        self.roster[pl_id] = [player_dict[pl_id], BEGIN, END]
                else:
                    pl_id = parsed_data.a['href'][11:-5]
                    if player_dict.has_key(pl_id):
                        self.roster[pl_id] = [player_dict[pl_id], BEGIN, END]

        # store all transactional date for the year, put data in helper func
        data = team_transactions.find(attrs={'class':'page_index'})
        for transaction in data.find_all('li'):
            # get date that transaction occurred
            date = convert_date.conversion(transaction.span.string)
            # if date occurs during season
            if date is not None and date>=BEGIN and date<=END:
                # get details of transactions
                for detail in transaction.find_all(attrs={'class':'transaction'}):
                    transaction_type=None
                    for string in detail.strings:
                        transaction_type = string[:7]
                        break
                    # get players and teams part of transaction
                    # links represent players, teams
                    links = []
                    for link in detail.find_all('a'):
                        links.append(link)
                    if len(links) == 0:
                        links.append(None)
                    # place in helper function
                    self._helper(date, str(transaction_type), links)

    def _helper(self, date, transaction_type, links):
        """
        Helper function to map different transactions to different functions
        for parsing
        """
        if transaction_type == "Traded ":
            self._trade(date, links)
        elif transaction_type == "As part":
            self._multi_trade(date, links)
        elif transaction_type == "Signed " or transaction_type == "Claimed":
            self._add(date, links[0])
        elif transaction_type == "Release" or transaction_type == "Waived ":
            self._remove(date, links[0])
        else:
            pass

    def _add(self, date, link):
        """
        Function that updates the date a certain player entered the team
        """
        if link is not None:
            pl_id = link['href'][11:-5]
            if self.roster.has_key(pl_id):
                self.roster[pl_id][1] = date
    
    def _remove(self, date, link):
        """
        Function that updates the date a certain player left the team
        """
        if link is not None:
            pl_id = link['href'][11:-5]
            if self.roster.has_key(pl_id):
                self.roster[pl_id][2] = date

    def _trade(self, date, links):
        """
        Function that updates the dates for players traded to and from the team
        """
        # breakpoint represents when the links received from the soup object
        # become players traded to the team instead of traded from
        # trade format: players traded from team, team traded with, 
        #   players traded to team
        # parses information based on that format
        breakpoint = False
        if links[0] is not None:
            for link in links:
                # check if link to a team or player
                if str(link['href'][11:-5]) != str(self.year):
                    if breakpoint:
                        self._add(date, link)
                    else:
                        self._remove(date, link)
                else:
                    breakpoint = True
    
    def _multi_trade(self, date, links):
        """
        Function that updates the dates for players traded to and from the team
        in multi-team deals
        """
        if links[0] is not None:
            for i in range(len(links)):
                # if the link represents the team trading players is the same
                # as the current team object
                if links[i].get('data-attr-from') == self.team_name:
                    i+=1
                    # remove all players from team until new team link occurs
                    while links[i].get('data-attr-to') is None:
                        self._remove(date, links[i])
                        i+=1
                # if the link represents the team acquiring players is the same
                # as the current team object
                elif links[i].get('data-attr-to') == self.team_name:
                    temp = i-1
                    # add all players from team until new team link occurs
                    while links[temp].get('data-attr-from') is None:
                        self._add(date, links[temp])
                        temp-=1
                else:
                    pass

    def make_teammates(self):
        """
        Function that matches players with new teammates, updating a player
        object's teammate dict
        """
        # for all players in the roster
        for pl in self.roster:
            # for all teammates in the roster
            for teammate in self.roster:
                # if a teammate is not current player
                if pl != teammate:
                    # if player start date is before teammate's exit date
                    # and if player exit date is before teammate's start
                    # date
                    if (self.roster[pl][1] < self.roster[teammate][2] and
                            self.roster[pl][2] > self.roster[teammate][1]):
                        # if the teammate doesn't already exist
                        if self.roster[pl][0].teammates.get(teammate) is None:
                            # update teammate dict of current player
                            # key = teammate id, value = (team, year)

                            # value is not a Player object, due to bugs 
                            # that occur when pickling recursive data structures
                            value = [[self.team, str(self.year)]]
                            self.roster[pl][0].update_teammates(teammate,
                                    value)
                        else:

                            value = self.roster[pl][0].teammates[teammate]
                            value.append([self.team, str(self.year)])
                            self.roster[pl][0].update_teammates(teammate,
                                    value)

def full_teammates():
    """
    Function that iterates through all teams available, creating their roster
    and updates teammates for all players on that team. Returns completed 
    dictionary of players (with teammates)
    """
    for t in teams:
        if type(t) is str:
            for year in range(B_YEAR, E_YEAR+1):
                print("Going through %d %s" % (year, t))
                _t = Team(t, year)
                _t.make_teammates()
        else:
            for year in range(t[1], t[2]+1):
                print("Going through %d %s" % (year, t[0]))
                _t = Team(t[0], year)
                _t.make_teammates()

    return player_dict
