from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import re

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
CORS(app)
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd
        

@app.route('/')
def index():
    return "Jeanette Rotich"

@app.route("/api/users", methods=["GET", "POST", "DELETE"])
def users():
    method = request.method
    if (method.lower() == "get"):
        users = Users.query.all()
        # gettin all values from db
        return jsonify([{"id": i.id, "username": i.username, "email": i.email, "password": i.pwd} for i in users])
    elif (method.lower() == "post"):
        try:
            username = request.json["username"]
            email = request.json["email"]
            pwd = request.json["pwd"]
            if (username and pwd and email):
                try:
                    user = Users(username, email, pwd)
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({"success": True})
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "Invalid form"})
    elif (method.lower() == "delete"): # DESTROY
        try:
            uid = request.json["id"]
            if (uid):
                try:
                    user = Users.query.get(uid) # Gets user with id = uid (because id is primary key)
                    db.session.delete(user) # Delete the user
                    db.session.commit() # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})
        
def getUsers():
    users = Users.query.all()
    return [{"id": i.id, "username": i.username, "email": i.email, "password": i.pwd} for i in users]

def addUser(username, email, pwd):
    if (username and pwd and email):
        try:
            user = Users(username, email, pwd)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

def removeUser(uid):
    uid = request.json["id"]
    if (uid):
        try:
            user = Users.query.get(uid)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False
    
@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["pwd"]
        if (email and password):
            users = getUsers()
            # Check if user exists
            return jsonify(len(list(filter(lambda x: x["email"] == email and x["password"] == password, users))) == 1)
        else:
            return jsonify({"error": "Invalid form"})
    except:
        return jsonify({"error": "Invalid form"})

@app.route("/api/register", methods=["POST"])
def register():
    try:
        email = request.json["email"]
        email = email.lower()
        password = request.json["pwd"]
        username = request.json["username"]
        # Check to see if user already exists
        users = getUsers()
        if(len(list(filter(lambda x: x["email"] == email, users))) == 1):
            return jsonify({"error": "Invalid form"})
        # Email validation check
        if not re.match(r"[\w\._]{5,}@\w{3,}.\w{2,4}", email):
            return jsonify({"error": "Invalid form"})
        addUser(username, email, password)
        return jsonify({"success": True})
    except:
        return jsonify({"error": "Invalid form"})
    
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    title = db.Column(db.String(256))
    content = db.Column(db.String(2048))



if __name__ == "__main__":
    app.run(debug=True)

