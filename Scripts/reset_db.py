import sqlite3
from typing import List

#get list of emails from file
with open('dummy_data/emails.txt','r') as e_File:
    emailList: List = e_File.read().split('\n')
    emailList = list(set(emailList))

#get list of constraints from file
with open('dummy_data/not_allowed.txt','r') as na_File:
    forbiddenPairsRaw: List = na_File.read().split('\n')
    forbiddenPairsRaw = list(set(forbiddenPairsRaw))

print(forbiddenPairsRaw)
#turn list of strings into list of tuples
constraintList: List = []
for i in range(len(forbiddenPairsRaw)):
    a, b = forbiddenPairsRaw[i].strip("()").replace("'","").split(',')
    constraintList.append((a,b))
    try:
        emailList.index(a)
    except ValueError:
        raise SystemExit("The name %r is in not_allowed.txt, but not in emails.txt" % a)
    try:
        emailList.index(b)
    except ValueError:
        raise SystemExit("The name %r is in not_allowed.txt, but not in emails.txt" % b)


pathToDB: str = '../db/allYourSantaAreBelongToUs.db'
#open connection to database
connection = sqlite3.connect(pathToDB)
dbCursor = connection.cursor()

#completely empty out the database
dbCursor.execute("DELETE FROM people")
dbCursor.execute("DELETE FROM forbiddenPairings")
#reset autoincrement
dbCursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='people';")
dbCursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='forbiddenPairings';")

#populate databases
for name in emailList:
    dbCursor.execute("""
INSERT INTO people (email)
VALUES (%r);""" % name)

for constraint in constraintList:
    dbCursor.execute("""
INSERT INTO forbiddenPairings (santa, assignment)
VALUES (%r, %r);""" %(constraint[0], constraint[1]))

connection.commit()
connection.close()