
import rlcompleter
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
import re
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
    quick_error=""
    custom_error=""
    if request.method == "POST":
        if "build-roll" in request.form:
            if not request.form.get('custom-name'):
                return render_template("/index.html", quick_error="", custom_error="Must include roll name.")
            if not request.form.get('custom-roll'):
                return render_template("/index.html", quick_error="", custom_error="Must include custom roll.")

        if "calculate" in request.form:
            # Check for input
            if not request.form.get('dice-roll'):
                return render_template("/index.html", quick_error="Must include dice roll", custom_error="")
            
            # Solve roll
            roll = request.form.get('dice-roll')
            solved = solve_roll(roll)
            
            # Check for error codes
            if "Invalid" in solved:
                if "Characters" in solved:
                    return render_template("/index.html", quick_error="Must only include the following characters: 0-9, d, +, -", custom_error="")
                if "Format" in solved:
                    return render_template("/index.html", quick_error="Invalid formatting.", custom_error="")
            
            return render_template("/index.html", quick_error=quick_error, custom_error="", solved=solved)
                    
    else:
        solved = {
            "raw": "",
            "total": ""
        }
        
        return render_template("/index.html", quick_error="", custom_error="", solved="")

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