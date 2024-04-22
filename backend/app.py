from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"

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



if __name__ == "__main__":
    app.run(debug=True)