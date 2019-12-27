#standard libraries
import random
from typing import Dict, List, TypeVar, Generic
import sqlite3

N = TypeVar('N')

class Node(object):
# create a node that represents a person
    def __init__(self, name_list1: List, name_list2: List):
        self.to_list: List = list(name_list1)   #list of people that Node may be assigned to
        self.from_list: List = list(name_list2) #list of people that may be assigned to Node
        self.assigned_to: int = None          #track who Node is assigned to
        self.assigned_from: int = None        #track who is assigned to Node
   
    def remove_edge_from(self, node: int):      
    #remove a name from list of incoming edges to the node
        self.from_list.remove(node)
    
    def remove_edge_to(self, node: int):       
    #remove a name from the list of outgoing edges from the node
        self.to_list.remove(node)
        
def permute_list(ordered_list: List) -> List:       
#ensure nondeterministic outputs
        old_list: List = list(ordered_list)
        new_list: List = []
        
        for i in range(len(old_list)):
            randIndex: int = random.randint(0, len(old_list) - 1)
            new_list.append(old_list.pop(randIndex))
         
        return new_list

def santa_assign(emails: List, not_allowed: List) -> List:
    nodeHash: dict = {}
    # dictionary mapping <name> to the Node that represents <name>
    emails_to_list: List = permute_list(emails)
    emails_from_list: List = permute_list(emails) #randomize
    for email in emails:
        # create node, then ensure that a person is not assigned to themselves
        nodeHash[email] = Node(emails_to_list,emails_from_list)
        nodeHash[email].remove_edge_from(email)
        nodeHash[email].remove_edge_to(email)
        
    for i,j in not_allowed:
        # ensure compliance with restricted pairings
        nodeHash[i].remove_edge_to(j)
        nodeHash[j].remove_edge_from(i)
        
    n: int = 0
    m: int = 0
    
    while True:
        # use depth first search to find a suitable assignment for everyone
        activeNode: N = nodeHash[emails[n]]
        if nodeHash[activeNode.to_list[m]].assigned_from == None:
            # assign the mth person on the nth persons to_list has been assigned, if they are available
            activeNode.assigned_to = activeNode.to_list[m]
            nodeHash[activeNode.assigned_to].assigned_from = emails[n]
            n += 1
            m = 0
            if n == len(emails):
            # if the algorithm has assigned someone to the nth person, then a solution has been found
                solution: dict = {}
                for email in emails:
                    solution[email] = nodeHash[email].assigned_to
                return solution
        elif m < len(activeNode.to_list) - 1:
            # if the mth person on the nth person's to_list was unavailable, increment m
            m += 1
        else:
            # if everyone on the nth person's to_list has been assigned, decrement n until an assignment can be made
            while True:
                n -= 1
                if n == -1:
                    # if the algorithm cycles backwards to the first person, and there is no one left on their to_list, then there is no solution
                    return "No solution available"
                activeNode = nodeHash[emails[n]]
                m = activeNode.to_list.index(activeNode.assigned_to) + 1
                nodeHash[activeNode.assigned_to].assigned_from = None
                activeNode.assigned_to = None
                if m < len(activeNode.to_list):
                    break
                
        
pathToDB: str = '../db/allYourSantaAreBelongToUs.db'

try:
    #open connection to database
    with sqlite3.connect(pathToDB) as connection:
        dbCursor = connection.cursor()
        #get emails from database
        dbCursor.execute("SELECT person_ID FROM people;")
        rawEmails: List = dbCursor.fetchall()
        #get constraints from database
        dbCursor.execute("SELECT santa_ID, assignment_ID FROM forbiddenPairings;")
        raw_constraints: List = dbCursor.fetchall()
except:
    raise SystemExit("There was an error. You need to run this script from Santabot/scripts")
    
#cleanse elements of rawEmails
email_list: List = []
for i in range(len(rawEmails)):
    email_list.append(rawEmails[i][0])
  
#cleanse elements of raw_constraints
constraint_list: List = []
for i in range(len(raw_constraints)):
    a: int = raw_constraints[i][0]
    b: int = raw_constraints[i][1]
    constraint_list.append((a,b))

# create assignements
santa_web = santa_assign(permute_list(email_list),constraint_list)

#put assignments into database
try:
    #open connection to database
    with sqlite3.connect(pathToDB) as connection:
        dbCursor = connection.cursor()
        for ID in email_list:
            dbCursor.execute('UPDATE people SET givingTo_ID = ? WHERE person_ID = ?', (santa_web[ID], ID))
except:
    raise SystemExit("There was an error. You need to run this script from Santabot/scripts")