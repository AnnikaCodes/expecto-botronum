"""a SQL-based chatlogger developed specifically for Expecto Botronum
    based on the ps-client chatlogger
    written by Annika"""

import sqlite3
from datetime import datetime
from typing import Union
import html
import pytz

import psclient

TYPES_TO_LOG = ['chat', 'pm']

class Chatlogger:
    """Class for logging chat to a SQL database

        Args:
            path (string): the path to the log database
    """
    def __init__(self, path):
        """Creates a new Chatlogger"""

        self.dbConnection = sqlite3.connect(path)
        self.SQL = self.dbConnection.cursor() # (acronym) pylint: disable=invalid-name

    def handleMessage(self, message):
        """Handles logging a message to chatlogs

        Args:
            message (Message): the Message
        """
        if message.type not in TYPES_TO_LOG: return
        room = message.room.id if message.room else None
        self.insert(self.messageToList(room, message))

    def search(self, roomID, userID="", oldest=0, keywords=None):
        """Searches chatlogs

        Args:
            roomID (str): The ID of the room to search in.
            userID (str, optional): The ID of the user whose messages are being searched for. Defaults to "".
            oldest (int, optional): The oldest timestamp to get
            keywords (List[str], optional): Keywords that must be included. Defaults to None.

        Returns:
            dictionary: a dictionary of matched messages
            (formatted as ``{date (string): [userid|time|type|senderName|body] (list of day's results)}``)
        """
        results = {}
        query = 'SELECT * FROM logs WHERE roomid = ?'
        args = [roomID]

        if userID:
            query += ' AND userid = ?'
            args.append(userID)

        for keyword in (keywords or []):
            query += " AND lower(body) LIKE '%' || ? || '%'"
            args.append(keyword)

        query += ' AND timestamp > ? ORDER BY timestamp DESC'
        args.append(oldest)

        dbResults = self.SQL.execute(query, args).fetchall()
        for result in dbResults:
            (log_id, timestamp, userid, username, kind, roomid, body) = result # pylint: disable=unused-variable
            date = str(datetime.fromtimestamp(timestamp).date())
            if date not in results: results[date] = []
            results[date].append(f"{userid}|{timestamp}|{kind}|{username}|{body}")

        print(query)
        return results

    def messageToList(self, room: Union[str, None], message: psclient.Message) -> tuple:
        """Formats a message for logging in the data format (timestamp, userid, username, kind, roomid, body)

        Args:
            message (Message): the message to format

        Returns:
            tuple: the formatted message
        """
        if message.time:
            time = datetime.utcfromtimestamp(int(message.time)).astimezone(pytz.utc).timestamp()
        else:
            time = datetime.timestamp(datetime.utcnow())

        return (
            int(time),
            str(message.sender.id) if message.sender else None,
            str(message.type),
            str(message.senderName) if message.senderName else None,
            psclient.toID(room) if room else None,
            str(message.body) if message.body else None
        )

    def insert(self, message: tuple) -> None:
        """Inserts a message into the SQL database

        Args:
            message (tuple): the message in the format (timestamp, userid, username, kind, roomid, body)
        """
        self.SQL.execute("INSERT INTO logs (timestamp, userid, username, type, roomid, body) VALUES (?, ?, ?, ?, ?, ?)", message)
        self.dbConnection.commit()

    def formatData(self, data, isHTML=False):
        """Formats data to text

        Args:
            data (string of form userid|time|type|senderName|body): the data
            isHTML (bool, optional): Whether to format as HTML. Defaults to False.

        Returns:
            string: a human-readable version of the message
        """
        splitData = data.split("|", 4)
        if len(splitData) == 5:
            userID, time, msgType, senderName, body = splitData
        elif len(splitData) == 3:
            userID, msgType, body = splitData
            time = ""
            senderName = userID
        else:
            psclient.log(f"DEBUG: unexpected number of data items (expected 5 or 3, got {str(len(splitData))}; data: f{data})")
            return "Unparseable message (bad format)"
            # TODO: figure out what to do about |html|, |raw|, etc

        try:
            time = f"[{str(datetime.utcfromtimestamp(int(time)).time())}] "
            if isHTML: time = f"<small>{html.escape(time)}</small>"
        except ValueError:
            time = ""
        body = body.strip().strip('\n')
        sender = senderName.strip()
        if isHTML:
            body = html.escape(body)
            sender = html.escape(sender)

        isAdmin = sender[:5] == '&amp;' if sender else False
        htmlRankSet = set(psclient.ranksInOrder)
        htmlRankSet.discard('&') # '&' rank is already handled with isAdmin
        if sender and (isAdmin or sender[0] in htmlRankSet.union(set('+%@*#~'))):
            rank = sender[:5] if isAdmin else sender[0]
            sender = f"<small>{rank}</small><b>{sender[len(rank):]}</b>" if isHTML else rank + sender[len(rank):]
        else:
            sender = f"<b>{sender}</b>"
        if msgType in ['chat', 'pm']: return f"{time}{sender}: {body}"
        if msgType == 'join': return f"{time}{sender} joined"
        if msgType == 'leave': return f"{time}{sender} left"
        return "Unparseable message"

    def __str__(self):
        return f"Chatlogger logging to a SQLite database ({str(self.dbConnection)})"
