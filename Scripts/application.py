import sqlite3
import json
from typing import Dict, List, Tuple
from flask import Flask, request
app = Flask(__name__)

path_to_db = '../db/allYourSantaAreBelongToUs.db'

@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/api/v1/person', methods = ["GET","POST"])
def return_all_people():
    
    if request.method == "POST":
        # add person to database
        posted_email = request.get_json()['email']
        with sqlite3.connect(path_to_db) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT into people (email) VALUES (?);', (posted_email,))            
    
    # return a json of all people
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        #get all of the people
        cursor.execute('SELECT person_ID, email, givingTo_ID FROM people')
        raw_data: List = cursor.fetchall()
        data: List = []
        for entry in raw_data:
            data.append({"person_ID": entry[0], "email": entry[1], "assignment ID": entry[2]})
        json_data = json.dumps(data)
    return json_data
    
@app.route('/api/v1/person/<person_id>', methods = ["GET","DELETE"])
def return_person(person_id: str) -> str:
    if request.method == "DELETE":
        with sqlite3.connect(path_to_db) as connection: 
            cursor = connection.cursor()
            try:
                command = 'DELETE FROM people WHERE person_ID=?;'
                cursor.execute(command, (person_id,))
                command = 'DELETE FROM forbiddenPairings WHERE santa_ID=? or assignment_ID=?;'
                cursor.execute(command, (person_id, person_id))
            except:
                return('There was an error. Check that the requested ID is valid.')
        return return_all_people()
    
    if request.method == "GET":
        # returns a json of <person_id>
        with sqlite3.connect(path_to_db) as connection: 
            cursor = connection.cursor()
            try:
                command = 'SELECT person_ID, email, givingTo_ID FROM people WHERE person_ID=?;'
                cursor.execute(command, (person_id,))
                raw_data: Tuple = cursor.fetchone()
                data: List = [{"person_ID": raw_data[0], "email": raw_data[1], "assignment ID": raw_data[2]}]
                json_data = json.dumps(data)
            except:
                return('There was an error. Check that the requested ID is valid.')
        return json_data
    
@app.route('/api/v1/forbidden_pairing', methods = ["GET","POST"])
def return_forbidden_pairings():
    
    if request.method == "POST":
        new_giver_constraint = request.get_json()["santa"]
        new_receiver_constraint = request.get_json()["assignment"]
        with sqlite3.connect(path_to_db) as connection:
            cursor = connection.cursor()
            command = 'SELECT (person_ID) FROM people WHERE email = ?;'
            cursor.execute(command, (new_giver_constraint,))
            giver_ID = cursor.fetchone()[0]
            cursor.execute(command, (new_receiver_constraint,))
            receiver_ID = cursor.fetchone()[0]
            command = 'INSERT into forbiddenPairings (santa, santa_ID, assignment, assignment_ID) VALUES (?, ?, ?, ?);'
            cursor.execute(command, (new_giver_constraint, giver_ID, new_receiver_constraint, receiver_ID))            
    
    # returns a json of all forbidden pairings
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT constraint_ID, santa, santa_ID, assignment, assignment_ID FROM forbiddenPairings;')
        raw_data: List = cursor.fetchall()
        data: List = []
        for pair in raw_data:
            data.append({"constraint_ID": pair[0], "santa": pair[1], "santa_ID": pair[2], "assignment": pair[3], "assignment_ID": pair[4]})
        json_data = json.dumps(data)
    return json_data
    
@app.route('/api/v1/forbidden_pairing/<id>')
def return_pairing(id: str) -> str:
    if request.method == 'DELETE':
        with sqlite3.connect(path_to_db) as connection: 
            cursor = connection.cursor()
            try:
                command = 'DELETE FROM forbiddenPairings WHERE constraint_ID=?;'
                cursor.execute(command, (id,))
            except:
                return('There was an error. Check that the requested ID is valid.')
        return return_forbidden_pairings()
    
    # returns a json of specified ID
    if request.method == 'GET':
        with sqlite3.connect(path_to_db) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT constraint_ID, santa, santa_ID, assignment, assignment_ID FROM forbiddenPairings WHERE constraint_ID=?;', (id,))
                raw_data: Tuple = cursor.fetchone()
                data: List = [{"constraint_ID": raw_data[0], "santa": raw_data[1], "santa_ID": raw_data[2], "assignment": raw_data[3], "assignment_ID": raw_data[4]}]
                json_data = json.dumps(data)
            except:
                return('There was an error. Check that the requested ID is valid.')
        return json_data