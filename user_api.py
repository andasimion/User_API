import sqlite3
import uuid
import time
import json
import models
from repository import UserRepo
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
    repo = UserRepo(db)
    users = repo.get_users()
    users_dicts = [user.json_dict() for user in users]
    json_body = json.dumps(users_dicts)
    close_db(db)
    return Response(json_body, mimetype='application/json')

@app.route('/user/<guid>', methods = ['GET'])
def get_user(guid):
    db = open_db()
    repo = UserRepo(db)
    user = repo.get_user(guid)
    user_dict = user.json_dict()
    json_body = json.dumps(user_dict) 
    close_db(db)  
    return Response(json_body, mimetype='application/json')

@app.route('/user', methods = ['POST'])
def add_user():
    db = open_db()
    repo = UserRepo(db)
    user_dict = json.loads(request.data)
    user = models.User(str(uuid.uuid4()), user_dict['first_name'], user_dict['last_name'], str(time.time()))
    user_inserted = repo.add_user(user)
    close_db(db)
    return "ok"
    
@app.route('/user/<guid>', methods = ['DELETE'])
def remove_user(guid):
    db = open_db()
    repo = UserRepo(db)
    removing_a_user = repo.remove_user(guid)
    close_db(db)
    return "ok"
    
@app.route('/user/<guid>', methods = ['PATCH', 'PUT'])
def modify_user(guid):
    user_dict = json.loads(request.data)
    allowed_params = ['first_name', 'last_name']
    update_sql = ", ".join([str(key)+ "= '" + str(user_dict.get(key)) + "'"  for key in user_dict.keys() if key in allowed_params])
    #column1 = value1, column2 = value2...., columnN = valueN
    db = open_db()
    repo = UserRepo(db)
    updating_the_user = repo.modify_user(guid, update_sql)
    db = open_db()
    updated_user = repo.get_user(guid)
    updated_user_dict = updated_user.json_dict()
    json_body = json.dumps(updated_user_dict)
    close_db(db)
    return Response(json_body, mimetype='application/json')
       
if __name__ == '__main__':
    app.run(debug = True)
