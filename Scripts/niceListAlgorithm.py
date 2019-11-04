import random #needed for random assignment

class Node(object):
# create a node that represents a person
    def __init__(self, name_list):
        self.to_list = list(name_list)   #list of people that Node may be assigned to
        self.from_list = list(name_list) #list of people that may be assigned to Node
        self.assigned_to = None          #track who Node is assigned to
        self.assigned_from = None        #track who is assigned to Node
    
    def removeEdgeFrom(self, node):      #remove a name from list of incoming edges to the node
        self.from_list.remove(node)
    
    def removeEdgeTo(self, node):        #remove a name from the list of outgoing edges from the node
        self.to_list.remove(node)
        
def permuteList(ordered_list):           #ensure nondeterministic outputs by permuting list of emails
        old_list = list(ordered_list)
        new_list = []
        
        for i in range(len(old_list)):
            randIndex = random.randint(0, len(old_list) - 1)
            new_list.append(old_list.pop(randIndex))
         
        return new_list

def santaAssign(emails, not_allowed):
    nodeHash = {}   #dictionary where key is string <email> and value is node representing <email>
    for email in emails:
        nodeHash[email] = Node(emails) #create a node for <email>
        nodeHash[email].removeEdgeFrom(email) #make sure person cannot have themselves
        nodeHash[email].removeEdgeTo(email)
        
    for i,j in not_allowed:     #make sure that nobody can be assigned to someone they don't want
        nodeHash[i].removeEdgeTo(j)
        nodeHash[j].removeEdgeFrom(i)
        
    n = 0
    m = 0
    
    while True:
        activeNode = nodeHash[emails[n]]
        
        if nodeHash[activeNode.to_list[m]].assigned_from == None: #check if mth person in activeNode's list of possible people is unassigned
            activeNode.assigned_to = activeNode.to_list[m]
            nodeHash[activeNode.assigned_to].assigned_from = emails[n]
            n += 1
            m = 0
            if n == len(emails): #if all n people have been assigned, then a viable solution has been found
                solution = []
                for email in emails:
                    solution.append((email,nodeHash[email].assigned_to))
                return solution
        elif m < len(activeNode.to_list) - 1: #if mth person is unavailable, check next person
            m += 1
        else: #if none of the people in activeNode's list of possible people are available, then unassign the previous node and increment m, decrement n
            while True:
                n -= 1
                assignment = nodeHash[emails[n]].assigned_to
                if n == -1:
                    return "No can do"
                k = nodeHash[emails[n]].to_list.index(assignment)
                nodeHash[assignment].assigned_from = None
                assignment = None
                m = k + 1
                if m < len(nodeHash[emails[n]].to_list):
                    break
                
        
emailList = ["Joe", "Will", "Charlotte", "Janet","Caitlin"]
forbiddenPairs = [('Joe','Caitlin'),('Caitlin','Joe'),('Caitlin','Janet'),('Joe','Charlotte')]
print santaAssign(permuteList(emailList),forbiddenPairs)
