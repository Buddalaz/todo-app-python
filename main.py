from flask import Flask, redirect, request, render_template, session

app = Flask(__name__)

app.secret_key = "super secret key"

app.config["SQLAL"]

@app.route("/")
def index():
    return render_template("index.html")
    # return "Hello world"


@app.route("/task")
def task():
    logged_user = session["username"]
    return render_template("task.html", username=logged_user)
    # return "Hello world"


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session["username"] = None
        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect("/task")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
