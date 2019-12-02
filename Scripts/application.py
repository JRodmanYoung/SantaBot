import sqlite3
import json
from typing import Dict
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/api/v1/person')
def return_people():
    # returns a json of all people
    with sqlite3.connect('../db/allYourSantaAreBelongToUs.db') as connection:
        cursor = connection.cursor()
        #get all of the people
        cursor.execute('SELECT * FROM people')
        raw_data: List = cursor.fetchall()
        data: Dict = {}
        for person in raw_data:
            data[person[0]] = {"email": person[1], "assignment ID": person[2]}
        json_data = json.dumps(data)
    return json_data
    
@app.route('/api/v1/person/<person_id>')
def return_person(person_id):
    # returns a json of <person_id>
    with sqlite3.connect('../db/allYourSantaAreBelongToUs.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM people WHERE person_ID={person_id}')
        raw_data: List = cursor.fetchall()
        data: Dict = {raw_data[0][0]:{"email": raw_data[0][1], "assignment ID": raw_data[0][2]}}
        json_data = json.dumps(data)
    return json_data
    
@app.route('/api/v1/person/forbidden_pairing')
def return_forbidden_pairings():
    # returns a json of all forbidden pairings
    with sqlite3.connect('../db/allYourSantaAreBelongToUs.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM forbiddenPairings')
        raw_data: List = cursor.fetchall()
        data: Dict = {}
        for pair in raw_data:
            data[pair[0]] = {"santa": pair[1], "santa_ID": pair[2], "assignment": pair[3], "assignment_ID": pair[4]}
        json_data = json.dumps(data)
    return json_data
    
@app.route('/api/v1/person/forbidden_pairing/<id>')
def return_pairing(id):
    # returns a json of specified ID
    with sqlite3.connect('../db/allYourSantaAreBelongToUs.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM forbiddenPairings WHERE constraint_ID={id}')
        raw_data: List = cursor.fetchall()
        data: Dict = {raw_data[0][0]:{"santa": raw_data[0][1], "santa_ID": raw_data[0][2], "assignment": raw_data[0][3], "assignment_ID": raw_data[0][4]}}
        json_data = json.dumps(data)
    return json_data
