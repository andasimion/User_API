from models import User, user_from_row
import uuid
from flask import request

# repo deals only with db stuff

class UserRepo:
    def __init__(self, db):
        self.db = db

    def get_users(self):
        cursor = self.db.cursor()
        sql = 'SELECT * FROM users'
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [user_from_row(row) for row in rows]
        
    def get_user(self, guid):
        cursor = self.db.cursor()
        sql = "SELECT * FROM users WHERE guid = '" + str(guid) + "'"
        cursor.execute(sql)
        row = cursor.fetchone()
        return user_from_row(row)
        
    def add_user(self, user):
        cursor = self.db.cursor()
        sql = "INSERT INTO users VALUES ('" + str(user.guid) + "', '" + user.first_name + "', '" + user.last_name + "', '" + str(user.created_at) + "')"
        cursor.execute(sql)
        self.db.commit()
    
    def remove_user(self, guid):
        cursor = self.db.cursor()
        sql = "DELETE FROM users WHERE guid = '" + str(guid) + "'"
        cursor.execute(sql)
        self.db.commit()
        
    def modify_user(self, guid, update_sql):
        cursor = self.db.cursor()
        sql = "UPDATE users SET " + update_sql + " WHERE guid = '" + guid + "'"
        cursor.execute(sql)
        self.db.commit()
        
        
