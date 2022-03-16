
from flask import Flask, redirect, render_template, request

# Configure flask
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    theme = "light"
    if request.args.get("darkmode") != None:
        theme = "dark"

    return render_template("/index.html", theme=theme)

if __name__ == '__main__':
	app.run(debug=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("/register")

