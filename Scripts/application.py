import sqlite3
import json
from typing import Dict, List, Tuple
from flask import Flask, request, abort, jsonify
from collections import defaultdict

app = Flask(__name__)

path_to_db = '../db/allYourSantaAreBelongToUs.db'
BAD_REQUEST_ERROR = 400

@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/api/v1/person')
def get_persons():
       
    # return a json of all people
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        #get all of the people
        cursor.execute(
            'SELECT person_ID, email, givingTo_ID, first_name, last_name '
            'FROM people')
        raw_data: List = cursor.fetchall()
        data: List = []
        for entry in raw_data:
            data.append(
                {"person_ID": entry[0],
                "email": entry[1],
                "assignment ID": entry[2],
                "first_name": entry[3],
                "last_name": entry[4]})
        json_data = json.dumps(data)
    return json_data
        
@app.route('/api/v1/person', methods = ["POST"])
def post_person():
    
    # verify that request contains a valid request  
    try:
        request_json: Dict = request.get_json()
    except:
        abort(
            BAD_REQUEST_ERROR ,
            description = "Please verify that request contains valid json.")
    try:
        posted_email = request_json['email']
    except:
        abort(
            BAD_REQUEST_ERROR,
            description = "Please verify that  request contains an email.")
    
    # add person to database         
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        # first_name and last_name may or may not be in the request
        request_json = defaultdict(lambda: None, request_json)
        command = ('INSERT into people (email, first_name, last_name) '
                   'VALUES (?, ?, ?);')
        
        cursor.execute(
            command,
            (
                posted_email,
                request_json['first_name'],
                request_json['last_name']
                ))
        
        # return posted record
        cursor.execute('SELECT (person_ID, email, givingTo_ID, first_name, '
                       'last_name) FROM people WHERE '
                       'person_ID=last_insert_rowid();')
        posted_record: List = cursor.fetchone()
        data: Dict = {
            "person_ID": posted_record[0],
            "email": posted_record[1],
            "givingTo_ID": posted_record[2], 
            "first_name": posted_record[3],
            "last_name": posted_record[4]}
        return json.dumps(data)
 
@app.route('/api/v1/person/<person_id>')
def get_person(person_id: str) -> str:   
    
    # returns a json of <person_id>
    with sqlite3.connect(path_to_db) as connection: 
        cursor = connection.cursor()
        try:
            command = 'SELECT person_ID, email, givingTo_ID FROM people ' \
                      'WHERE person_ID=?;'
            cursor.execute(command, (person_id,))
            raw_data: Tuple = cursor.fetchone()
            data: List = [
                {
                    "person_ID": raw_data[0],
                    "email": raw_data[1],
                    "assignment ID": raw_data[2]}]
            json_data = json.dumps(data)
        except:
            return(
                'There was an error. Check that the requested ID is valid.')
    return json_data
    
@app.route('/api/v1/person/<person_id>', methods = ["DELETE"])
def delete_person(person_id: str) -> str:
    
    with sqlite3.connect(path_to_db) as connection: 
        cursor = connection.cursor()
        try:
            cursor.execute(
                'DELETE FROM people WHERE person_ID=?;',
                (person_id,))
            command = 'DELETE FROM forbiddenPairings WHERE santa_ID=? or ' \
                      'assignment_ID=?;'
            cursor.execute(command, (person_id, person_id))
        except:
            return(
            'There was an error. Check that the requested ID is valid.')
    return "user has been removed from database"

@app.route('/api/v1/forbidden_pairing')
def get_forbidden_pairings():
    
    # returns a json of all forbidden pairings
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT constraint_ID, santa, santa_ID, assignment, '
                       'assignment_ID FROM forbiddenPairings;')
        raw_data: List = cursor.fetchall()
        data: List = []
        for pair in raw_data:
            data.append(
                {
                    "constraint_ID": pair[0],
                    "santa": pair[1],
                    "santa_ID": pair[2],
                    "assignment": pair[3],
                    "assignment_ID": pair[4]})
        json_data = json.dumps(data)
    return json_data
        
@app.route('/api/v1/forbidden_pairing', methods = ["POST"])
def post_forbidden_pairing():
    
    # verify that request is valid
    try:
        request_json = request.get_json()
    except:
        abort(
            BAD_REQUEST_ERROR,
            description = "Please verify that request contains valid json.")
    try:
        new_giver_constraint = request_json['santa_ID']
    except:
        abort(
            BAD_REQUEST_ERROR,
            description = "Please verify that request contains a "
                          "'santa_ID' key.")
    try:
        new_receiver_constraint = request_json['assignment_ID']
    except:
        abort(
            BAD_REQUEST_ERROR,
            description = "Please verify that request contains an "
                          "'assignment_ID' key.")
    
    with sqlite3.connect(path_to_db) as connection:
        # add new constraint to database
        cursor = connection.cursor()
        command = 'SELECT email FROM people WHERE person_ID = ?;'
        cursor.execute(command, (new_giver_constraint,))
        giver_ID = cursor.fetchone()[0]
        cursor.execute(command, (new_receiver_constraint,))
        receiver_ID = cursor.fetchone()[0]
        command = ('INSERT into forbiddenPairings (santa, santa_ID, '
                   'assignment, assignment_ID) VALUES (?, ?, ?, ?);')
        cursor.execute(
            command,
            (
                new_giver_constraint,
                giver_ID,
                new_receiver_constraint,
                receiver_ID))
         
        #return posted record
        cursor.execute('SELECT constraint_ID, santa, santa_ID, assignment,'
                       ' assignment_ID FROM forbiddenPairings WHERE '
                       'constraint_ID=last_insert_rowid();')
        posted_record: List = cursor.fetchone()
        data: Dict = {
            "constraint_ID": posted_record[0],
            "santa": posted_record[1],
            "santa_ID": posted_record[2], 
            "assignment": posted_record[3],
            "assignment_ID": posted_record[4]}
        return json.dumps(data)

@app.route('/api/v1/forbidden_pairing/<id>')
def get_forbidden_pairing(id: str) -> str:   
 
    # returns a json of specified ID
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        try:
            command = ('SELECT constraint_ID, santa, santa_ID, assignment, '
                       'assignment_ID FROM forbiddenPairings WHERE '
                       'constraint_ID=?;')
            cursor.execute(command, (id,))
            raw_data: Tuple = cursor.fetchone()
            data: List = [
                {
                    "constraint_ID": raw_data[0],
                    "santa": raw_data[1],
                    "santa_ID": raw_data[2],
                    "assignment": raw_data[3],
                    "assignment_ID": raw_data[4]}]
            json_data = json.dumps(data)
        except:
            return('There was an error. Check that the requested ID is '
                   'valid.')
    return json_data
        
@app.route('/api/v1/forbidden_pairing/<id>', methods = ['DELETE'])
def delete_forbidden_pairing(id: str) -> str:

    with sqlite3.connect(path_to_db) as connection: 
        cursor = connection.cursor()
        try:
            cursor.execute(
                'DELETE FROM forbiddenPairings WHERE constraint_ID=?;',
                (id,))
        except:
            return('There was an error. Check that the requested ID is '
                   'valid.')
    return "constraint has been deleted"

@app.errorhandler(BAD_REQUEST_ERROR)
def resource_not_found(err):
    return jsonify(error=str(err)), BAD_REQUEST_ERROR