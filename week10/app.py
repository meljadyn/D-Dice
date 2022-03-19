
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL

# Configure flask
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies) -- CREDIT TO CS50 TEAM, FINANCE PSET
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Reload when changes occur
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure SQL database
#db = SQL("sqlite:///project.db")

@app.route("/", methods=["GET", "POST"])
def index():
    theme = "light"
    quick_error=""
    custom_error=""

    if request.args.get("darkmode") != None:
        theme = "dark"

    return render_template("/index.html", theme=theme, quick_error="", custom_error="")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear active session
    session.clear()

    # If directed to login
    if request.method == "GET":
        return render_template("/login.html", error="")

    # If login was attempted
    else:
        # If username/password was not submitted
        if not request.form.get("username"):
            return render_template("/login.html", error="You must provide a username.")
        if not request.form.get("password"):
            return render_template("/login.html", error="You must provide a password")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("/register.html")


@app.route("/security", methods=["GET", "POST"])
def security():
    return render_template("/security.html")

if __name__ == '__main__':
	app.run(debug=True)