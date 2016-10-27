-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (id serial PRIMARY KEY,
                      name varchar(100) NOT NULL);

CREATE TABLE matches (p1 int REFERENCES players(id),
                      p2 int REFERENCES players(id),
                      winner int REFERENCES players(id));

CREATE VIEW standings AS
SELECT id,
       name,
       (SELECT count(*) 
        FROM matches WHERE players.id = matches.winner) AS wins,

       (SELECT count(*) 
        FROM matches WHERE players.id = matches.p1
        OR players.id = matches.p2) AS matches
        FROM players
        ORDER BY wins DESC;