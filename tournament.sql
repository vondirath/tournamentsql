-- This is creating the database and it will drop it if one exists.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (id serial PRIMARY KEY,
                      name varchar(100) NOT NULL);

CREATE TABLE matches (p1 int REFERENCES players(id),
                      p2 int REFERENCES players(id));

CREATE VIEW standings AS
SELECT id,
       name,
       (SELECT count(*) 
        FROM matches WHERE players.id = matches.p1) AS wins,

       (SELECT count(*) 
        FROM matches WHERE players.id = matches.p1
        OR players.id = matches.p2) AS matches
        FROM players
        ORDER BY wins DESC;