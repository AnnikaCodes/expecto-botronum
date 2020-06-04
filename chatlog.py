import config
import core

import pathlib
from datetime import datetime

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
            str((datetime.utcfromtimestamp(int(message.time)) if message.time else datetime.utcnow()).time()).split('.', 1)[0],
            str(message.type) if message.type else '',
            str(message.senderName) if message.senderName else '',
            (str(message.body) if message.body else '') + '\n'
        ])

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {}
    
    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Chatlog module: handles chatlogging. Commands: " + ", ".join(self.commands.keys())