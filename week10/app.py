
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
import re

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
    if request.method == "POST":
        if "build-roll" in request.form:
            if not request.form.get('custom-name'):
                return render_template("/index.html", quick_error="", custom_error="Must include roll name.")
            if not request.form.get('custom-roll'):
                return render_template("/index.html", quick_error="", custom_error="Must include custom roll.")

        if "calculate" in request.form:
            # check for a result
            if not request.form.get('dice-roll'):
                return render_template("/index.html", quick_error="Must include dice roll", custom_error="")
            
            # remove all spaces, makes it lower case, remove any + or - at the beginning or end
            roll = request.form.get('dice-roll')
            roll = roll.replace(' ', '')
            roll = roll.lower()

            # check for valid characters
            for i in range(len(roll)):
                if not roll[i].isdecimal():
                    if roll[i] != "+" and roll[i] != "-" and roll[i] != "d":
                        return render_template("/index.html", quick_error="Must only include the following characters: 0-9, d, +, -", custom_error="")

            # Format dice roll into list of lists
            try:
                roll = format_roll(roll)
            except:
                return render_template("/index.html", quick_error="Invalid formatting.", custom_error="")
            
            if "invalid" in roll:
                return render_template("/index.html", quick_error="Invalid formatting.", custom_error="")
            
            return render_template("/index.html", quick_error="all is well", custom_error="")
        
    else:
        return render_template("/index.html", quick_error="", custom_error="")

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

# Formats plain string of roll info into a list of lists (i.e. "1d4+12d6-3" is now [['+', '1', 'd', '4'], ['+', '12', 'd', '6'], ['-', '3']])
def format_roll(roll):
    roll = roll.strip()
    roll = roll.rstrip('+')
    roll = roll.rstrip('-')

    # Split at + or - symbol
    final = re.split("(\+|\-)", roll)

    # Attach - or + symbol to start of next item
    while "-" in final or "+" in final:
        for i in range(len(final)):
            if final[i] == "-":
                final[i+1] = "m" + final[i+1]
                final.pop(i) 
                break
            if final[i] == "+":
                final[i+1] = "a" + final[i+1]
                final.pop(i) 
                break
            
    # Replace instances of "m" and "a" with appropriate symbol
    for i in range(len(final)):
        final[i] = final[i].replace("m", "-")
        final[i] = final[i].replace("a", "+")

    # Ensure every item has an operator
    for i in range(len(final)):
        if final[i][0] != "+" and final[i][0] != "-":
            final[i] = "+" + final[i]

    # Check if any section has more than one "d", making it invalid
    for i in range(len(final)):
        if final[i].count("d") > 1:
            return "invalid, multiple d"
        if re.search("\d", final[i]) == None:
            return "invalid, missing number"
            
    # Split each individual dice roll into a list (ex. +12d4 is now ['+', '12', 'd', '4'])
    for i in range(len(final)):
        final[i] = re.split("(\+|\-|d)",final[i])
        
    for i in range(len(final)):  # Remove any white space from the split function
        while '' in final[i]:
            final[i].remove('')

    for i in final:
        if len(i) != 4 and len(i) != 2:
            return "invalid unknown"

    return final


if __name__ == '__main__':
	app.run(debug=True)