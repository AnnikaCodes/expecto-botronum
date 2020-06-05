import config
import core

import pathlib
from datetime import datetime
import pytz

####### chatlog.py #######
## handles logging chat ##
## by Annika            ##
##########################

class Chatlogger:
    """Class for logging chat
    """    
    def __init__(self, path):
        """Creates a new Chatlogger

        Args:
            path (string): the path to the logging directory
        """        
        self.path = pathlib.Path(path)
        if not self.path.exists(): self.path.mkdir()
        if not self.path.is_dir(): core.log("E: Chatlogger(): logging directory is a file: " + self.path.as_posix())
    
    def handleMessage(self, message):
        """Handles logging a message

        Args:
            message (Message): the Message
        """
        if not config.logchat: return
        room = message.room.id if message.room else 'global'
        logFile = self.getFile(room, 'a')
        logFile.write(self.formatMessage(message))
    
    def getFile(self, roomid, perms):
        """Returns a file object corresponding to the room.

        Args:
            roomid (string that is an ID): the room
            perms (string): the file perms (i.e.)

        Returns:
            File: a file for the log file for that room and day
        """
        roomFolderPath = self.path.joinpath(roomid)
        if not roomFolderPath.exists(): roomFolderPath.mkdir()
        if not roomFolderPath.is_dir(): 
            return core.log("E: Chatlogger(): logging directory is a file: " + roomFolderPath.as_posix())
        filePath = roomFolderPath.joinpath(str(datetime.now().date()) + '.txt')
        return filePath.open(perms)
    
    def formatMessage(self, message):
        """Formats a message for logging.
        Format: userid|time|type|senderName|body
        Args:
            message (Message): the message to format

        Returns:
            (string): the formatted message
        """
        return "|".join([
            str(message.sender.id) if message.sender else '',
            str(int(datetime.utcfromtimestamp(int(message.time)).astimezone(pytz.utc).timestamp())) if message.time else str(int(datetime.timestamp(datetime.utcnow()))),
            str(message.type) if message.type else '',
            str(message.senderName) if message.senderName else '',
            (str(message.body) if message.body else '') + '\n'
        ])
    
    def search(self, roomid="", userid="", keyword=""):
        """Searches chatlogs

        Args:
            roomid (str, optional): The ID of the room to search in. Defaults to "".
            userid (str, optional): The user. Defaults to "".
            keyword (str, optional): [description]. Defaults to "".

        Returns:
            dictionary: a dictionary of matched messages (formatted as {date (string): [userid|time|type|senderName|body] (list of day's results)})
        """        
        results = {}
        searchDir = self.path.joinpath(roomid)
        userSearch = (userid + '|') if userid else ""
        if roomid and searchDir.is_dir():
            for logFilePath in searchDir.iterdir():
                date = logFilePath.name.strip(".txt")
                for line in logFilePath.open('r').readlines():
                    try:
                        if line[:len(userSearch)] == userSearch and keyword in line.split('|',4)[4]: 
                            if date not in results.keys(): 
                                results[date] = [line]
                            else:
                                results[date].append(line)
                    except IndexError:
                        pass
        return results
    
    def formatData(self, data):
        """Formats data to text

        Args:
            data (string of form userid|time|type|senderName|body): the data

        Returns:
            string: a human-readable version of the message
        """        
        userid, time, msgType, senderName, body = data.split("|", 4)
        try:
            time = "[" + str(datetime.utcfromtimestamp(int(time)).time()) + "] "
        except ValueError:
            time = ""
        if msgType in ['chat', 'pm']:
            return time + "{sender}: {body}".format(
                sender = senderName.strip(),
                body = body.strip().strip('\n')
            )
        elif msgType == 'join':
            return time + "{sender} joined".format(sender = senderName.strip())
        elif msgType == 'leave':
            return time + "{sender} left".format(sender = senderName.strip())
        else:
            return "Unparseable message"
