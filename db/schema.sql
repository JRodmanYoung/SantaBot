CREATE TABLE people
(
	person_ID 			INTEGER PRIMARY KEY AUTOINCREMENT,
	email				VARCHAR NOT NULL UNIQUE,
	givingTo_ID			INTEGER
	first_name			VARCHAR
	last_name			VARCHAR
);

CREATE TABLE forbiddenPairings
(
	constraint_ID 		INTEGER PRIMARY KEY AUTOINCREMENT,
	santa				VARCHAR NOT NULL,
	santa_ID			INTEGER NOT NULL,
	assignment			VARCHAR NOT NULL,
	assignment_ID		INTEGER NOT NULL,
	FOREIGN KEY(santa_ID) REFERENCES people(person_ID)
	FOREIGN KEY(assignment_ID) REFERENCES people(person_ID)
);