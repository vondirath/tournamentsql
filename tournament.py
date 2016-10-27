#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


@contextmanager
def get_cursor():
    """
    Query helper function using contextlib to create a
    cursor from a database connection object, performing queries.
    """
    DB = connect()
    cursor = DB.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        DB.commit()
    finally:
        cursor.close()
        DB.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print ("Connection Failed")


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as cursor:
        cursor.execute("select count(*) from players;")
        results = cursor.fetchall()
        for row in results[0]:
            return row


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as cursor:
        cursor.execute("insert into players (name) values (%s)", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player
    in first place, or a player tied for first place
    if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with get_cursor() as cursor:
        cursor.execute("select * from standings;")
        results = cursor.fetchall()
        return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as cursor:
        query = "insert into matches (p1, p2) values (%s, %s);"
# prevents SQL injection attacks
        outcome = (winner, loser,)
        cursor.execute(query, outcome)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    lista = playerStandings()
    pairings = []
    for x in range(0, len(lista), 2):
        (id1, name1, wins1, matches1) = lista[x]
        (id2, name2, wins2, matches2) = lista[x + 1]
        pairings.append((id1, name1, id2, name2))
    return pairings
