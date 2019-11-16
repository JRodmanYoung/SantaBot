CREATE TABLE people
(
	ID 		INTEGER PRIMARY KEY AUTOINCREMENT,
	email	VARCHAR NOT NULL UNIQUE
);

CREATE TABLE forbiddenPairings
(
	ID 			INTEGER PRIMARY KEY AUTOINCREMENT,
	santa		VARCHAR NOT NULL,
	assignment	VARCHAR NOT NULL,
	FOREIGN KEY(santa) REFERENCES people(email)
	FOREIGN KEY(assignment) REFERENCES people(email)
);