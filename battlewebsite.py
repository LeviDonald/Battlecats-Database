import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session

DATABASE_FILE = "battlecats.db"
HOME_HTML = "home.html"

app = Flask(__name__)
app.secret_key = "d2uhewduewhdjjsiwsjwdiIssakwa12091"


# Connecting to database function (returns cursor and connection)
def connect_database(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return conn, cur


# Home page
@app.route("/")
def home():
    return render_template(HOME_HTML)


# Starts application
if __name__ == '__main__':
    app.run(debug=True)