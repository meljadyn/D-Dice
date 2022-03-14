import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get current user's username
    rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = rows[0]["username"]

    # Get user's portfolio from database
    portfolio = db.execute("SELECT * FROM portfolio WHERE username = ?", username)
    user = db.execute("SELECT cash FROM users WHERE username = ?", username)

    # Add name, price and total to portfolio
    for i in range(0, len(portfolio)):
        look = lookup(portfolio[i]["symbol"])
        portfolio[i]["name"] = look["name"]
        portfolio[i]["price"] = look["price"]
        portfolio[i]["total"] = (look["price"] * portfolio[i]["shares"])

    # Add final total (stocks + cash) to user
    user[0]["total"] = user[0]["cash"]
    for i in range(0, len(portfolio)):
        user[0]["total"] += portfolio[i]["total"]

    # Send user and info to the page
    return render_template("/index.html", portfolio=portfolio, user=user)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        symbol = symbol.upper()

        # Return apology if invalid
        if shares.isdigit() == False:
            return apology("must only input whole numbers")
        shares = int(shares)
        if not symbol:
            return apology("must input symbol")
        symbol_info = lookup(symbol)
        if symbol_info == None:
            return apology("symbol not found")
        if not shares:
            return apology("must input number of shares")
        if shares < 1:
            return apology("must purchase 1 or more shares")

        # Reject purchases if client doesn't have enough cash
        user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = user[0]["cash"]
        price = symbol_info["price"]

        if len(user) == 0:
            return apology("server error: username not detected")
        if cash < (price * shares):
            return apology("you can not afford these shares")

        # Record transaction in databse
        else:
            time = datetime.now()
            time = time.strftime("%b. %d, %Y at %H:%M:%S")

            # Get current user's username
            rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
            username = rows[0]["username"]

            # Add purchase into purchase history
            db.execute("INSERT INTO history (username, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)",
                       username, symbol, shares, price, time)

            # Update user's cash
            db.execute("UPDATE users SET cash = ? WHERE username = ?", (cash - (price * shares)), username)

            # If current stock is in this user's portfolio, add stock
            in_portfolio = db.execute("SELECT symbol, shares FROM portfolio WHERE username = ? AND symbol = ?", username, symbol)

            if len(in_portfolio) < 1:
                db.execute("INSERT INTO portfolio (username, symbol, shares) VALUES (?, ?, ?)", username, symbol, shares)

            # If current stock is not in user's portfolio, update number of shares
            else:
                old_shares = in_portfolio[0]["shares"]
                db.execute("UPDATE portfolio SET shares = ? WHERE username = ? AND symbol = ?",
                           (old_shares + shares), username, symbol)

            return redirect("/")

    else:
        return render_template("/buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get current user's username
    rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = rows[0]["username"]

    # Get user's history from database
    history = db.execute("SELECT * FROM history WHERE username = ?", username)

    return render_template("/history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbol = symbol.upper()

        # Require that the user enters a symbol
        if not symbol:
            return apology("Must include symbol")

        # Check if symbol exists
        symbol_info = lookup(symbol)
        if symbol_info != None:

            # Send the information and user to display page
            return render_template("quoted.html", symbol=symbol_info)

        # If request method is GET
        else:
            return apology("Symbol not found.")

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Require that a user enters a username (from text field name="username")
        if not username:
            return apology("must provide username")

        # Apology for already existing username
        if len(db.execute("SELECT id FROM users WHERE username = ?", username)) > 0:
            return apology("username already exists")

        # Require that the user enters a password and confirmation (text field: psssword)
        if not password:
            return apology("must provide password")

        if not confirmation:
            return apology("must confirm password")

        # Apology for passwords not matching
        if password != confirmation:
            return apology("passwords must match")

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
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get current user's username
    rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = rows[0]["username"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Check the values
        if not symbol:
            return apology("must select a valid stock")
        if not shares:
            return apology("must input number of shares")
        if shares < 1:
            return apology("must input 1 or more shares")

        # Check valid stock/shares is selected
        in_portfolio = db.execute("SELECT * FROM portfolio WHERE symbol LIKE ? AND username = ?", symbol, username)
        in_users = db.execute("SELECT cash FROM users WHERE username = ?", username)

        if len(in_portfolio) != 1:
            return apology("must select a valid stock.")
        if shares > in_portfolio[0]["shares"]:
            return apology("you don't own that many shares")

        symbol = symbol.upper()

        # Find stock price
        look = lookup(symbol)
        price = look["price"]
        cash = in_users[0]["cash"]

        time = datetime.now()
        time = time.strftime("%b. %d, %Y at %H:%M:%S")

        # Update user's cash
        db.execute("UPDATE users SET cash = ? WHERE username = ?",
                   (cash + (price * shares)), username)

        # Update user's history
        db.execute("INSERT INTO history (username, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)",
                   username, symbol, (0 - shares), price, time)

        # Update user's portfolio
        db.execute("UPDATE portfolio SET shares = ? WHERE username = ? AND symbol = ?",
                   (in_portfolio[0]["shares"] - shares), username, symbol)

        return redirect("/")

    # If user arrives here via GET
    else:
        portfolio = db.execute("SELECT symbol FROM portfolio WHERE username = ?", username)

        # Send user to sell page with the data required to make it function
        return render_template("sell.html", portfolio=portfolio)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to your account"""

    if request.method == "POST":
        cash = request.form.get("cash")

        # Return apology if invalid
        if not cash:
            return apology("must input total")
        try:  # check if input can be converted to float
            cash = float(cash)
        except (KeyError, TypeError, ValueError):
            return apology("must include only numbers and decimal points")

        if cash < 1:
            return apology("must add more than $1.00")

        # Check client's current cash total
        user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        old_cash = user[0]["cash"]

        # Update client's cash total
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash + old_cash), session["user_id"])

        return redirect("/")

    else:
        # Get current user's username
        rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = rows[0]["username"]

        # Get user's cash and portfolio from database
        portfolio = db.execute("SELECT symbol, shares FROM portfolio WHERE username = ?", username)
        user = db.execute("SELECT cash FROM users WHERE username = ?", username)

        # Add cash total to portfolio
        for i in range(0, len(portfolio)):
            look = lookup(portfolio[i]["symbol"])
            portfolio[i]["total"] = (look["price"] * portfolio[i]["shares"])

        # Add final total (stocks + cash) to user
        user[0]["total"] = user[0]["cash"]
        for i in range(0, len(portfolio)):
            user[0]["total"] += portfolio[i]["total"]

        # Send user and info to the page
        return render_template("/addcash.html", user=user)
