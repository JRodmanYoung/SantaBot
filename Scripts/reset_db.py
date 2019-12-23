import sqlite3
from typing import List

#get list of emails from file
with open('dummy_data/emails.txt','r') as e_File:
    email_list: List = e_File.read().split('\n')
    email_list = list(set(email_list))

#get list of constraints from file
with open('dummy_data/not_allowed.txt','r') as na_File:
    forbidden_pairs_raw: List = na_File.read().split('\n')
    forbidden_pairs_raw = list(set(forbidden_pairs_raw))

#turn list of strings into list of tuples
constraint_list: List = []
for i in range(len(forbidden_pairs_raw)):
    tuple_list: List = forbidden_pairs_raw[i].strip("()").replace("'","").split(',')
    constraint_list.append((tuple_list[0],tuple_list[1]))
    try:
        email_list.index(tuple_list[0])
    except ValueError:
        raise SystemExit(f"The name {tuple_list[0]} is in not_allowed.txt, but not in emails.txt")
    try:
        email_list.index(tuple_list[1])
    except ValueError:
        raise SystemExit(f"The name {tuple_list[1]} is in not_allowed.txt, but not in emails.txt")
        
pathToDB: str = '../db/allYourSantaAreBelongToUs.db'

try:
    #open connection to database
    connection = sqlite3.connect(pathToDB)
    DB_cursor = connection.cursor()
    
    #completely empty out the database
    DB_cursor.execute("DELETE FROM people")
    DB_cursor.execute("DELETE FROM forbiddenPairings")
    
    #reset autoincrement
    DB_cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='people';")
    DB_cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='forbiddenPairings';")
  
    #populate databases, starting with table 'people'
    for name in email_list:
            DB_cursor.execute("INSERT INTO people (email) VALUES (?);", (name,))
    connection.commit()
    
    for constraint in constraint_list:
        #get ids of names  from 'people' table to populate 'forbiddenPairings'
        DB_cursor.execute("SELECT person_ID from people WHERE email = ?", (constraint[0],))
        DB_santaID: int = DB_cursor.fetchall()[0][0]
        DB_cursor.execute("SELECT person_ID from people WHERE email = ?", (constraint[1],))
        DB_assignmentID: int = DB_cursor.fetchall()[0][0]
        DB_cursor.execute("""
    INSERT INTO forbiddenPairings (santa, santa_ID, assignment, assignment_ID)
    VALUES (?,?,?,?);""", (constraint[0], DB_santaID, constraint[1], DB_assignmentID))
    connection.commit()
    connection.close()
except:
    raise SystemExit("You need to run this script from Santabot/scripts")