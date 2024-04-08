import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session, abort

# Ease of access constants for HTML files
DATABASE_FILE = "battlecats.db"
HOME_HTML = "home.html"
UNITS_HTML = "units.html"
UNIT_VIEW_HTML = "unit_view.html"
ERROR_HTML = "404_error.html"

app = Flask(__name__)
app.secret_key = "d2uhewduewhdjjsiwsjwdiIssakwa12091"

# How many images load per scroll
quantity = 10

# Remove these characters from unit names to get the correct image file
banned_characters = ['/', ':', '*', '?', '<', '>', '|']

 
def remove_characters(char_list, word):
    for char in char_list:
        word = word.replace(char, "")
    return word


# Connecting to database function (returns cursor and connection)
def connect_database(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return conn, cur


# 404 Error :() (shocked face)
@app.errorhandler(404)
def error_404(exception):
    return render_template(ERROR_HTML, exception=exception)

# Home page
@app.route("/")
def home():
    return render_template(HOME_HTML)


# Shows all units in alphabetical order
@app.route("/units")
def all_units():
    conn, cur = connect_database(DATABASE_FILE)
    cur.execute("SELECT cat_id, cat_first FROM battle_cat;")
    results = cur.fetchall()
    conn.close()
    for count, i in enumerate(results):
        i = list(i)
        i.insert(2, remove_characters(banned_characters, i[1]))
        results[count] = i
    return render_template(UNITS_HTML, results=results)


# Shows a singular unit with all of its stats + forms
@app.route("/unit-view/<int:unit_id>")
def unit(unit_id):
    try:
        conn, cur = connect_database(DATABASE_FILE)
        cur.execute("SELECT cat_first, cat_second, cat_trueform, cat_rarity_id FROM battle_cat WHERE cat_id = ?;", (unit_id,))
        # [0] - First form name, [1] - Second form name, [2] - Trueform name, [3] - Rarity ID
        results = cur.fetchone()
        for count, i in enumerate(results):
            i = list(i)
            i.insert(2, remove_characters(banned_characters, i[1]))
            results[count] = i
        cur.execute("SELECT rarity_name FROM cat_rarity WHERE rarity_id = ?;", (results[3],))
        rarity = cur.fetchone()[0]
        conn.close()
        return render_template(UNIT_VIEW_HTML, name1=results[0], name2=results[1], name3=results[2], rarity=rarity)
    except Exception as e:
        abort(404, e)

# Starts application
if __name__ == '__main__':
    app.run(debug=True)