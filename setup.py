from models import User
import sqlite3
import time
#it's run only once

def add_user(user):
    db = sqlite3.connect('users_db.db')
    cursor = db.cursor()
    sql = "INSERT INTO users VALUES ('" + str(user.guid) + "', '" + user.first_name + "', '" + user.last_name + "', '" + str(user.created_at) + "')"
    print sql
    cursor.execute(sql)
    db.commit()
    db.close()

user01 = User(None, "John", "Doe", time.time())
user02 = User(None, "Dan", "Doe", time.time())
    
add_user(user01)
add_user(user02)
