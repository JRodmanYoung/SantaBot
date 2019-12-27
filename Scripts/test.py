import sqlite3
from typing import List

path_to_db = '../db/allYourSantaAreBelongToUs.db'

with sqlite3.connect(path_to_db) as connection: 
            cursor = connection.cursor()
            command = 'SELECT person_ID, email, givingTo_ID FROM people WHERE person_ID=?;'
            cursor.execute(command, (1,))
            raw_data: List = list(cursor.fetchone())
            print(raw_data)
            print(type(raw_data))