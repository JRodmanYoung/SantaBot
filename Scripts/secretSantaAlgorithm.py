# Secret Santa Algorithm
# This file is outdated; please use niceListAlgorithm.py instead
import random

def santaAssign(emails, not_allowed):
    niceList = []
    santaHash = {}
    assignment = ''
    for name1 in emails:
        not_allowed.append((name1,name1))
        santaHash[name1] = []
        for name2 in emails:
            if not((name1,name2) in not_allowed):
                santaHash[name1].append(name2)
         
        assignment = random.choice(santaHash[name1])
        niceList.append((name1,assignment))
        for name in emails:
            not_allowed.append((name,assignment))
    return niceList 

print santaAssign(['Joe','Caitlin','Will','Charlotte','Janet'],[('Joe','Caitlin'),('Caitlin','Joe'),('Will','Joe')])