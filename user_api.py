import sqlite3
import json
import models
from flask import Flask, request, Response

# guid = global unique identifier

app = Flask(__name__)

def open_db():
    return sqlite3.connect('users_db.db')
    
def close_db(db):
    db.close()
    
@app.route('/user', methods = ['GET'])
def get_users():
    db = open_db()
    cursor = db.cursor()
    sql = 'SELECT * FROM users'
    cursor.execute(sql)
    rows = cursor.fetchall()
    users = [models.user_from_row(row) for row in rows]
    users_dicts = [user.json_dict() for user in users]
    json_body = json.dumps(users_dicts)
    close_db(db)
    return Response(json_body, mimetype='application/json')

@app.route('/user/<guid>', methods = ['GET'])
def get_user(guid):
    db = open_db()
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE guid ='" + str(guid) + "'"
    cursor.execute(sql)
    row = cursor.fetchone()
    user = models.user_from_row(row)
    user_dict = user.json_dict()
    json_body = json.dumps(user_dict) 
    close_db(db)  
    return Response(json_body, mimetype='application/json')

@app.route('/user', methods = ['POST'])
def add_user():
    print request.data
    user_dict = json.loads(request.data)
    user = models.User(user_dict['guid'], user_dict['first_name'], user_dict['last_name'])
    db = open_db()
    cursor = db.cursor()
    sql = "INSERT INTO users VALUES ('" + str(user.guid) + "', '" + user.first_name + "', '" + user.last_name + "')"
    print sql
    cursor.execute(sql)
    db.commit()
    close_db(db)
    return "ok"
    
@app.route('/user/<guid>', methods = ['DELETE'])
def remove_user(guid):
    db = open_db()
    cursor = db.cursor()
    sql = "DELETE FROM users WHERE guid = '" + str(guid) + "'"
    cursor.execute(sql)
    db.commit()
    close_db(db)
    return "ok"
       
if __name__ == '__main__':
    app.run(debug = True)