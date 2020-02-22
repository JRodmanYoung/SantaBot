#standard libraries
import random
from typing import List, Dict
import sqlite3

# A Node represents a person in a web.  Each node is connected to other nodes 
# representing the possible secret santa assignments.
class Node(object):
    
    def __init__(self, ID_list_1: List, ID_list_2: List):
        self.to_list: List = list(ID_list_1)    #list of outgoing connections
        self.from_list: List = list(ID_list_2)  #list of incoming connections
        self.assigned_to: int = None            #track who Node is assigned to
        self.assigned_from: int = None          #track who is assigned to Node
   
    def remove_edge_from(self, node: int):      
    #remove an ID from list of incoming connections to the node
        self.from_list.remove(node)
    
    def remove_edge_to(self, node: int):       
    #remove a name from the list of outgoing connections from the node
        self.to_list.remove(node)
 
#ensure nondeterministic outputs 
def permute_list(ordered_list: List) -> List:       
    old_list: List = list(ordered_list)
    new_list: List = []
        
    for i in range(len(old_list)):
        randIndex: int = random.randint(0, len(old_list) - 1)
        new_list.append(old_list.pop(randIndex))
     
    return new_list

def santa_assign(ID_numbers: List, not_allowed: List) -> List:
    nodeHash: Dict = {}  # dictionary that will map IDs to Node objects
    ID_to_list: List = permute_list(ID_numbers)
    ID_from_list: List = permute_list(ID_numbers)  #randomize
    for ID in ID_numbers:
        # create node, then ensure that a person is not assigned to themselves
        nodeHash[ID] = Node(ID_to_list,ID_from_list)
        nodeHash[ID].remove_edge_from(ID)
        nodeHash[ID].remove_edge_to(ID)
        
    for i,j in not_allowed:
        # ensure compliance with restricted pairings
        nodeHash[i].remove_edge_to(j)
        nodeHash[j].remove_edge_from(i)
        
    n: int = 0
    m: int = 0  # Will be used to create connections from 
    
    # use depth first search to find a suitable assignment for everyone
    while True:
        
        activeNode: Node = nodeHash[ID_numbers[n]]
        if nodeHash[activeNode.to_list[m]].assigned_from == None:
            # assign the active Node to the mth person on their to_list, if the
            # mth person is available
            activeNode.assigned_to = activeNode.to_list[m]
            nodeHash[activeNode.assigned_to].assigned_from = ID_numbers[n]
            n += 1
            m = 0
            if n == len(ID_numbers):
            # if the algorithm has assigned someone to the last person, then a
            # solution has been found
                solution: Dict = {}
                for ID in ID_numbers:
                    solution[ID] = nodeHash[ID].assigned_to
                return solution
        elif m < len(activeNode.to_list) - 1:
            # if the mth person on the nth person's to_list was unavailable,
            # check the next value of m
            m += 1
        else:
            # if everyone on the nth person's to_list has been assigned,
            # decrement n until an assignment can be made
            while True:
                n -= 1
                if n == -1:
                    # if the algorithm cycles backwards to the first person, and
                    # there is no one left on their to_list, then there is no
                    # solution
                    return "No solution available"
                activeNode = nodeHash[ID_numbers[n]]
                m = activeNode.to_list.index(activeNode.assigned_to) + 1
                nodeHash[activeNode.assigned_to].assigned_from = None
                activeNode.assigned_to = None
                if m < len(activeNode.to_list):
                    break
                
        
path_to_db: str = '../db/allYourSantaAreBelongToUs.db'

try:
    #open connection to database
    with sqlite3.connect(path_to_db) as connection:
        dbCursor = connection.cursor()
        #get IDs from database
        dbCursor.execute("SELECT person_ID FROM people;")
        raw_ID_list: List = dbCursor.fetchall()
        #get constraints from database
        dbCursor.execute(
            "SELECT santa_ID, assignment_ID FROM forbiddenPairings;")
        raw_constraints: List = dbCursor.fetchall()
except:
    raise SystemExit(
        "There was an error. You need to run this script from Santabot/scripts")

    
#cleanse elements of raw_ID_list
ID_list: List = []
for i in range(len(raw_ID_list)):
    ID_list.append(raw_ID_list[i][0])
  
#cleanse elements of raw_constraints
constraint_list: List = []
for i in range(len(raw_constraints)):
    a: int = raw_constraints[i][0]
    b: int = raw_constraints[i][1]
    constraint_list.append((a,b))

# create assignements
santa_web = santa_assign(permute_list(ID_list),constraint_list)

#put assignments into database
try:
    #open connection to database
    with sqlite3.connect(path_to_db) as connection:
        dbCursor = connection.cursor()
        for ID in ID_list:
            dbCursor.execute(
                'UPDATE people SET givingTo_ID = ? WHERE person_ID = ?',
                (santa_web[ID], ID))
except:
    raise SystemExit(
        "There was an error. You need to run this script from Santabot/scripts")