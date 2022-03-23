
import rlcompleter
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
import re
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint

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
    # Set variables
    quick_error=""
    custom_error=""
    
    # Get username
    rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = rows[0]["username"]

    # Load in the macro list
    macros = db.execute("SELECT id, roll_name, roll_text FROM rolls WHERE username = ?", username)

    if request.method == "POST":
        # If custom builder is being used
        if "build-roll" in request.form:
            # If the user is not logged in
            if not session.get("user_id"):
                return render_template("/index.html", custom_error="You must be logged in to use this function.")

            # Ensure that name and roll are defined
            if not request.form.get('custom-name'):
                return render_template("/index.html", custom_error="Must include roll name.", macros=macros)
            if not request.form.get('custom-roll'):
                return render_template("/index.html", custom_error="Must include custom roll.", macros=macros)
            
            # Define variables
            custom_name = request.form.get('custom-name')
            custom_roll = request.form.get('custom-roll')
            
            # Check if roll is valid
            test = solve_roll(custom_roll)
            if "Invalid" in test:
                if "Characters" in test:
                    return render_template("/index.html", custom_error="Must only include the following characters: 0-9, d, +, -", macros=macros)
                if "Format" in test:
                    return render_template("/index.html", custom_error="Invalid formatting.", macros=macros)

            # Insert roll into database
            db.execute("INSERT INTO rolls (username, roll_name, roll_text) VALUES(?, ?, ?)", username, custom_name, custom_roll)

            # Send user back to homepage
            return redirect("/")

        # If quick roller is being used
        if "calculate" in request.form:
            # If user is not logged in
            if not session.get("user_id"):
                custom_error="You must be logged in to use this function."
            else:
                custom_error=""

            # Check for input
            if not request.form.get('dice-roll'):
                return render_template("/index.html", quick_error="Must include dice roll", custom_error=custom_error, macros=macros)
            
            # Solve roll
            roll = request.form.get('dice-roll')
            solved = solve_roll(roll)
            
            # Check for error codes
            if "Invalid" in solved:
                if "Characters" in solved:
                    return render_template("/index.html", quick_error="Must only include the following characters: 0-9, d, +, -", custom_error="", macros=macros)
                if "Format" in solved:
                    return render_template("/index.html", quick_error="Invalid formatting.", custom_error=custom_error, macros=macros)
            
            return render_template("/index.html", custom_error=custom_error, solved=solved, macros=macros)

        # Rolling from the macro chart
        if "roll-it" in request.form:
            id = request.form.get("id")

            rows = db.execute("SELECT roll_text FROM rolls WHERE id = ?", id)
            roll_text = rows[0]["roll_text"]

            rolled = solve_roll(roll_text)
            if "Invalid" in rolled:
                if "Characters" in rolled:
                    return render_template("/index.html", custom_error="Must only include the following characters: 0-9, d, +, -", macros=macros)
                if "Format" in rolled:
                    return render_template("/index.html", custom_error="Invalid formatting.", macros=macros)

            return render_template("/index.html", custom_error="", rolled=rolled, macros=macros)
        
        if "delete-it" in request.form:
            id = request.form.get("id")
            db.execute("DELETE FROM rolls WHERE id = ?", id)
            return redirect("/")


    # If method = GET               
    else:
        # If the user is not logged in
        if not session.get("user_id"):
            return render_template("/index.html", custom_error="You must be logged in to save custom dice roll macros.")
        
        return render_template("/index.html", custom_error="", macros=macros)


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

        # Query database for username -- UP TO REDIRECT TO HOME PAGE WAS LEARNED FROM FINANCE'S LOGIN CODE
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("/login.html", error="Incorrect username or passowrd.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Require that a user enters a username (from text field name="username")
        if not username:
            return render_template("/register.html", error="You must provide a username")

        # Apology for already existing username
        if len(db.execute("SELECT id FROM users WHERE username = ?", username)) > 0:
            return render_template("/register.html", error="Username is taken.")

        # Require that the user enters a password and confirmation (text field: psssword)
        if not password:
            return render_template("/register.html", error="You must provide a password")

        if not confirmation:
            return render_template("/register.html", error="You must confirm your password")

        # Apology for passwords not matching
        if password != confirmation:
            return render_template("Your passwords must match")

        # Generate hash for password
        passhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Insert username and hashed password into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, passhash)

        # Find their user ID
        row = db.execute("SELECT id FROM users WHERE username = ?", username)
        username_id = row[0]["id"]

        # Log user in
        session["user_id"] = username_id
        return redirect("/")

    else:
        return render_template("register.html", error="")


def solve_roll(roll):
    roll = roll.replace(' ', '')
    roll = roll.lower()

    # check for valid characters
    for i in range(len(roll)):
        if not roll[i].isdecimal():
            if roll[i] != "+" and roll[i] != "-" and roll[i] != "d":
                return "Invalid: Characters"

    # Format dice roll into list of lists
    try:
        formatted_roll = format_roll(roll)
    except:
        return "Invalid: Formatting"
    
    if "invalid" in roll:
        return "Invalid: Formatting"
        
    # Evaluate the rolls
    raw_rolls = raw_roll(formatted_roll)

    # Format raw roll for printing
    formatted_raw = format_raw(raw_rolls)

    # Find total
    sum = find_sum(formatted_raw)

    # Make dictionary to return to main function
    roll_answers = {
        "raw": formatted_raw,
        "total": sum
    }

    return roll_answers


# Formats plain string of roll info into a list of lists (i.e. "1d4+12d6-3" is now [['+', '1', 'd', '4'], ['+', '12', 'd', '6'], ['-', '3']])
def format_roll(roll):
    
    # Remove trailing operators
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


def raw_roll(formattedRoll):
    roll = formattedRoll

    raw_rolls = []
    for i in range(len(roll)):

        # If a die needs to be rolled
        if len(roll[i]) == 4:
            operator = roll[i][0]
            n = int(roll[i][1])
            dice = int(roll[i][3])
            
            rolls = []
            for j in range(n):
                if operator == "-":
                    rolls.append("-" + str(randint(1, dice))) # add - when it appears
                else:
                    rolls.append(str(randint(1, dice)))
                
            raw_rolls.append(rolls)

        # If it's just a number
        if len(roll[i]) == 2:
            operator= roll[i][0]
            n = roll[i][1]
            raw_rolls.append(operator + n)

    return raw_rolls


def format_raw(rawRolls):
    rolls = rawRolls
    formatted = ""  

    for i in range(len(rolls)):
        if "-" in rolls[i]:
            formatted += rolls[i] + " "
        else:
            format = "+".join(rolls[i])
            formatted += format + " "
        
    formatted = formatted.strip()
    formatted = formatted.replace("++", "+")
    formatted = formatted.replace("+-", "-")
    formatted = formatted.replace(" ", ", ")

    return formatted


def find_sum(formattedRoll):
    formatted = formattedRoll
    sum_format = formatted.replace(', ', '+')
    sum_format = sum_format.replace('++', '+')
    sum_format = sum_format.replace('+-', '-')

    sum = eval(sum_format)

    return sum

if __name__ == '__main__':
	app.run(debug=True)