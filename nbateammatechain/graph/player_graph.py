from collections import defaultdict
from ..utils import serialize
import Queue

player_dict = serialize.load_pickle('raw_files/player_dict_full.pickle')

class Node(object):
    """
    A node object represents a player, but with added functionality for
    graph algorithms
    """
    def __init__(self, player):
        # A node's ID is the player it represents
        self.id = player
        self.prev = None
        self.visited = False

class Graph(object):
    """
    A graph of players, with an edge defined as a teammate
    """
    def __init__(self):
        
        # Create a dict of sets to represent graph
        # Key = object, Value = set of teammate objects
        self._graph = defaultdict(set)
        self._nodes = {}
        self._build_connections()


    def update_attr(self, attr = None, dict_key = None):
        """
        Store attributes user is searching for
        """
        self._attr = attr
        self._dict_key = dict_key

    def _build_connections(self):
        """
        Builds the graph and all edges between vertices
        """
        for player_id in player_dict:

            # get a players node if it exists, otherwise define it
            player_node = self._nodes.get(player_id)
            if player_node is None:
                # player is a Player instance, player_node is a Node instancee
                player = player_dict[player_id]
                player_node = Node(player)
                self._nodes[player_id] = player_node
            
            for teammate_id in player_node.id.teammates:
                
                # get a teammates node if it exists, otherwise define it
                teammate_node = self._nodes.get(teammate_id) 
                if teammate_node is None:
                    # teammate is a Player instance, teammate_node is a Node
                    # instance 
                    teammate = player_dict[teammate_id]
                    teammate_node = Node(teammate)
                    self._nodes[teammate_id] = teammate_node
                # create edge between a player and its teammate
                self._graph[player_node].add(teammate_node)
    
    def build_path(self, p1_id, p2_id):
        """
        User callable function to build path between two players based on
        specified attribute. Returns path
        """
        
        # Node objects
        player1 = self._nodes[p1_id]
        player2 = self._nodes[p2_id]
        
        # if the user defines an attribute
        if self._attr is not None:
            # find recursive solution to problem
            val = self._build_path_recursive("Begin", p1_id, p2_id)
            
            # reset function attributes
            func = self._build_path_recursive
            static_var_func = func.__func__
            static_var_func.counter = 0
            static_var_func.first = True
            static_var_func.res = list()

            return val
        # otherwise simply find smallest degree of separation between
        # two players (shortest path)
        else:
            # path of player1 to player2 
            # simple bfs algorithm
            path = []
            q = Queue.Queue()
            player1.visited = True
            q.put(player1)

            while not q.empty():
                player = q.get()
                if player is player2:
                    break
                
                for teammate in self._graph[player]:
                    if not teammate.visited:
                        teammate.visited = True
                        teammate.prev = player
                        q.put(teammate)
            
            player = player2
            while player is not None:
                path.append(player.id.uid)
                player=player.prev

            path.reverse()
            
            # destructor equivalent, reset node values
            dq = Queue.Queue()
            player1.visited = False
            dq.put(player1)
            while not dq.empty():
                player = dq.get()
                if player is player2:
                    break

                for teammate in self._graph[player]:
                    if teammate.visited:
                        teammate.visited = False
                        teammate.prev = None
                        dq.put(teammate)

            return path

    def _build_path_recursive(self, path, p1_id, p2_id) :
        """
        Recursively builds a path between two vertices until final vertex is
        reached. The minimum path between the two vertices is returned.
        If vertex not reachable under parameter(attribute) restrictions, None
        is returned.
        """
        # alias variables for recursive calls, c type static variables 
        func = self._build_path_recursive
        static_var_func = func.__func__
        
        # define static variables
        if not hasattr(static_var_func, "counter"):
            static_var_func.counter = 0
        if not hasattr(static_var_func, "first"):
            static_var_func.first = True
        if not hasattr(static_var_func, "res"):
            static_var_func.res = list()

        # Node instances
        player1 = self._nodes[p1_id]
        player2 = self._nodes[p2_id]
        
        # if path coming from build_path, initialize path
        if path == "Begin":
            path = []
        # if path in higher stack frame does not exist, return None
        if path is None:
            return None
        
        # determine if checking for a dictionary statistic/accomplishment, or
        # a regular value
        # update path by including (current player name, attribute value)
        # tuple
        if self._dict_key is None:
            path = path + [(player1.id.uid, getattr(player1.id, self._attr))]
        else:
            path = path + [(player1.id.uid, getattr(player1.id,
                self._attr).get(self._dict_key))]

        # base case
        if player1 is player2:
            return path
        
        # boolean to determine if a path is reachable at current stage
        path_exists = False
        # init. maximum attribute among current player's teammates
        max_attr = -1
        for teammate in self._graph[player1]:
            # if the teammate is not part of current path
            if not any(teammate.id.uid in n for n in path):
                # get maximum attribute value among teammates
                # check if path is reachable 
                attr_val = None
                if self._dict_key is None:
                    attr_val = getattr(teammate.id, self._attr)
                else:
                    attr_val = getattr(teammate.id, self._attr).get(self._dict_key)

                if attr_val is not None and attr_val > max_attr:
                    path_exists = True
                    max_attr = attr_val

        # path is not reachable if all teammates are in current path
        if not path_exists:
            return None

        # get a list of teammates that are equivalent to the maximum attribute
        # in teammate list
        max_attr_list = []
        for teammate in self._graph[player1]:
            if not any(teammate.id.uid in n for n in path):
                if self._dict_key is None:
                    attr_val = getattr(teammate.id, self._attr)
                else:
                    attr_val = getattr(teammate.id, self._attr).get(self._dict_key)

                if attr_val is not None and attr_val == max_attr:
                    max_attr_list.append(teammate.id.uid)

        # create a list of function args to call for each player that has a max
        # attribute 
        # done to determine smaller path
        func_list = []
        for i in max_attr_list:
            func_list.append((i,p2_id))
        
        # recursively call function, with p1_id being initialized to a teammate
        # equivalent to a max value attribute
        p = []
        for i in func_list:
            # only recursively call if first teammate or if the size of the path
            # from a teammate to player2 is greater than the current path,
            # where the teammate is a previous value in func_list such that
            # its minimum path length is being compared against
            if static_var_func.first or static_var_func.counter>len(path):
                p = func(path, *i)
                static_var_func.first = False
            
            if p is not None:
                if static_var_func.counter == 0:
                    static_var_func.counter = len(p)
                else:
                    if len(p) < static_var_func.counter:
                        static_var_func.counter = len(p)
            # if returned value is None, return None 
            else:
                return None
            # append p to resultant paths
            static_var_func.res.append(p)
        # resultant path should not include empty paths and should be unique
        result = []
        for i in static_var_func.res:
            if i not in result:
                result.append(i)
        if result.count([]) != 0:
            result.remove([])
       
        if len(result) == 0:
            return result
        # return minimum length path in result 
        return min(result, key=len)
