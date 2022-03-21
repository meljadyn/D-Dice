
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
db = SQL("sqlite:///dndice.db")

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    quick_error=""
    custom_error=""
    if "build-roll" in request.form:
        if not request.form.get('custom-name'):
            return render_template("/index.html", quick_error="", custom_error="Must include roll name.")
        if not request.form.get('custom-roll'):
            return render_template("/index.html", quick_error="", custom_error="Must include custom roll.")

    if "calculate" in request.form:
        # check for a result
        if not request.form.get('dice-roll'):
            return render_template("/index.html", quick_error="Must include dice roll", custom_error="")
        
        # remove all spaces and makes it lower case
        roll = request.form.get('dice-roll')
        roll = roll.replace(' ', '')
        roll = roll.lower()

        # check for valid characters
        for i in range(len(roll)):
            if not roll[i].isdecimal():
                if roll[i] != "+" and roll[i] != "-" and roll[i] != "d":
                    return render_template("/index.html", quick_error="Must only include the following characters: 0-9, d, +, -", custom_error="")

        # split roll into chunks separated by +
        dice = roll.split("+")
        
        for i in range(len(dice)):
            if "-" in dice[i]:
                ### remove the - section and put it somewhere else
                print("hi")
        

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
            error = "You must provide a username."
            return render_template("/login.html", error="You must provide a username.")
        if not request.form.get("password"):
            return render_template("/login.html", error="You must provide a password")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    return render_template("/register.html", error=error)


@app.route("/security", methods=["GET", "POST"])
def security():
    return render_template("/security.html")


if __name__ == '__main__':
	app.run(debug=True)