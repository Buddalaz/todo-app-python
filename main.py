from email.policy import default
import enum
from flask import Flask, redirect, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key = "super secret key"

db_path = os.path.join(os.path.dirname(__file__), 'app.db')

# app.config["SQLALCHEMY_DATABASE_URL"] = f"sqllite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqllite:///{db_path}"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    task = db.relationship('Task', backref="user", lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.OPENED)
    user_id = db.Column(db.Integer, db.Foriegnkey("user.id"))


class TaskStatus(enum.Enum):
    COMPLETE = "Complete"
    CLOSED = "Closed"
    OPENED = "Opened"


db.create_all()


@app.route("/")
def index():
    return render_template("index.html")
    # return "Hello world"


@app.route("/task", methods=["POST", "GET"])
def task():
    taskName = "Empty"
    status = "Empty"

    logged_user = session["user_id"]

    if request.method == "GET":
        task_list = Task.query.filter_by(user_id=logged_user)
    if request.method == "POST":
        if "task_name" in request.form:
            taskName = request.form["task_name"]
        if "status" in request.form:
            status = request.form["age"]
        if "user_id" in request.form:
            user_id = request.form["user_id"]

        task = Task(task=taskName, status=status, user_id=user_id)
        db.session.add(task)
        db.session.commit()

    return render_template("task.html", username=logged_user, task=task_list)
    # return "Hello world"


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session["user_id"] = None
        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        userName = request.form["username"]

        exsisting_user = User.query.filter_by(username=userName).first()
        print(exsisting_user)

        if exsisting_user is None:
            user = User(username=userName)
            db.session.add(user)
            db.session.commit()
            exsisting_user = user
            print(user.id)

        session["user_id"] = exsisting_user.id
        return redirect("/task")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
