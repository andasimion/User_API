import uuid
import sqlite3
import time

class User:
    def __init__(self, guid, first_name, last_name, created_at):
        if guid != None:
            self.guid = guid
        else:
            self.guid = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        
    def __repr__(self):
        return 'user' + repr((self.created_at, self.guid, self.first_name, self.last_name))
    
    #json dict contains only the atributes that we want to pass into the json representation
    def json_dict(self):
        return self.__dict__
        
def user_from_row(row):
    return User(row[0], row[1], row[2], row[3])


