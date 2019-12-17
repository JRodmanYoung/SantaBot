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

#turn list of strings into list of tuples
constraintList: List = []
for i in range(len(forbiddenPairsRaw)):
    tupleList: List = forbiddenPairsRaw[i].strip("()").replace("'","").split(',')
    constraintList.append((tupleList[0],tupleList[1]))
    try:
        emailList.index(tupleList[0])
    except ValueError:
        raise SystemExit(f"The name {tupleList[0]} is in not_allowed.txt, but not in emails.txt")
    try:
        emailList.index(tupleList[1])
    except ValueError:
        raise SystemExit(f"The name {tupleList[1]} is in not_allowed.txt, but not in emails.txt")
        
pathToDB: str = '../db/allYourSantaAreBelongToUs.db'

try:
    #open connection to database
    connection = sqlite3.connect(pathToDB)
    dbCursor = connection.cursor()
    
    #completely empty out the database
    dbCursor.execute("DELETE FROM people")
    dbCursor.execute("DELETE FROM forbiddenPairings")
    
    #reset autoincrement
    dbCursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='people';")
    dbCursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='forbiddenPairings';")
  
    #populate databases, starting with table 'people'
    for name in emailList:
            dbCursor.execute("INSERT INTO people (email) VALUES (?);", (name,))
    connection.commit()
    
    for constraint in constraintList:
        #get ids of names  from 'people' table to populate 'forbiddenPairings'
        dbCursor.execute("SELECT person_ID from people WHERE email = ?", (constraint[0],))
        DBsantaID: int = dbCursor.fetchall()[0][0]
        dbCursor.execute("SELECT person_ID from people WHERE email = ?", (constraint[1],))
        DBassignmentID: int = dbCursor.fetchall()[0][0]
        dbCursor.execute("""
    INSERT INTO forbiddenPairings (santa, santa_ID, assignment, assignment_ID)
    VALUES (?,?,?,?);""", (constraint[0], DBsantaID, constraint[1], DBassignmentID))
    connection.commit()
    connection.close()
except:
    raise SystemExit("You need to run this script from Santabot/scripts")