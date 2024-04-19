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

# How many images load per scroll (not functional yet)
quantity = 10

# Remove these characters from unit names to get the correct image file
banned_characters = ['/', ':', '*', '?', '<', '>', '|']


def duplicate_remover(dup_list):
    return list(dict.fromkeys(dup_list))


def remove_characters(char_list, word):
    for char in char_list:
        word = word.replace(char, "")
    return word


def frame_to_second(frames):
    return round((frames / 30), 2)


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
    try:
        return render_template(HOME_HTML)
    except Exception as e:
        abort(404, e)


# Shows all units in alphabetical order
@app.route("/units")
def all_units():
    try:
        conn, cur = connect_database(DATABASE_FILE)
        cur.execute("SELECT cat_id, cat_first FROM battle_cat ORDER BY cat_first ASC;")
        results = cur.fetchall()
        conn.close()
        for count, i in enumerate(results):
            i = list(i)
            i.insert(2, remove_characters(banned_characters, i[1]))
            results[count] = i
        return render_template(UNITS_HTML, results=results)
    except Exception as e:
        abort(404, e)


# Shows a singular unit with all of its stats + forms
@app.route("/unit-view/<int:unit_id>")
def unit(unit_id):
    conn, cur = connect_database(DATABASE_FILE)
    cur.execute("SELECT cat_first, cat_second, cat_trueform, cat_rarity_id, cat_experience FROM battle_cat WHERE cat_id = ?;", (unit_id,))
    # [0] - First form name, [1] - Second form name, [2] - Trueform name, [3] - Rarity ID, [4] - Cat experience
    results = cur.fetchone()
    if results:
        try:
            if results[2]:
                form_names = ["Normal", "Evolved", "True"]
            else:
                form_names = ["Normal", "Evolved"]
            results = list(results)
            cur.execute("SELECT rarity_name FROM cat_rarity WHERE rarity_id = ?;", (results[3],))
            rarity = cur.fetchone()[0]
            # Get all talent IDs from talent_bridge and get talent names from cat_talenttree
            cur.execute("SELECT talent_id FROM talent_bridge WHERE cat_id = ?;", (unit_id,))
            talents = cur.fetchall()
            if talents:
                talent_list = []
                for talent in talents:
                    cur.execute("SELECT talent_name FROM cat_talenttree WHERE talent_id = ?;", (talent[0],))
                    talent_list.append(cur.fetchone()[0])
            else:
                talent_list = []
            skill_list = []
            for i in range(1, 4):
                cur.execute("SELECT form_id, skill_id FROM skill_bridge WHERE cat_id = ? AND form_id = ?;", (unit_id, i))
                skills = duplicate_remover(cur.fetchall())
                skill_list.append(skills)
            # Get all skills from skill_bridge that has unit_id, find skill_name and skill_desc using IDs from skill_bridge then append to skill_list
            skill_info_list = []
            for count, skills in enumerate(skill_list):
                if skills:
                    for skill in skills:
                        cur.execute("SELECT skill_name, skill_description FROM cat_skills WHERE skill_id = ?;", (skill[1],))
                        skill_info = cur.fetchone()
                        # [0] - form_id, [1] - skill_name, [2] - skill_description
                        skill_info_list.append([skill[0], skill_info[0], skill_info[1]])
                    skill_list[count] = skill_info_list
                    skill_info_list = []
            # Get all types for each form
            type_list = []
            for i in range(1, 4):
                cur.execute("SELECT type_id FROM type_bridge WHERE cat_id = ? AND form_id = ?;", (unit_id, i))
                type_id = cur.fetchall()
                current_list = []
                for enemy_type in type_id:
                    cur.execute("SELECT type_name FROM cat_type WHERE type_id = ?;", (enemy_type[0],)) 
                    current_list.append(cur.fetchone()[0])
                type_list.append(current_list)
            # Get all the different prices for each cat including different form prices
            cur.execute("SELECT cost FROM cat_cost WHERE cat_id = ?;", (unit_id,))
            cat_costs = cur.fetchall()
            # Checking if the current unit evolves via. evolution materials
            cur.execute("SELECT ingredient_id, ingredient_amount FROM trueform_bridge WHERE cat_id = ?;", (unit_id,))
            trueform_materials = cur.fetchall()
            if trueform_materials:
                for count, material in enumerate(trueform_materials):
                    cur.execute("SELECT ingredient_name FROM trueform_ingredient WHERE ingredient_id = ?;", (material[0],))
                    trueform_materials[count] = [cur.fetchone()[0], material[1]]
                # Only give trueform experience amount to units that are from Rare - Legend Rare
                if results[3] <= 4:
                    cur.execute("SELECT experience FROM trueform_experience WHERE rarity_id = ?;", (results[3],))
                    trueform_experience = cur.fetchone()[0]
                else:
                    trueform_experience = None
            else:
                # Assigns something to trueform_experience so the program doesn't break
                trueform_experience = None
            # Adds Image applicable names
            image_names = []
            for i in range(0, 3):
                if results[i] is not None:
                    image_names.append(remove_characters(banned_characters, results[i]))
            stat_list = []
            for i in range(1, len(form_names)+1):
                cur.execute("SELECT hp, attack, attack_range, attack_frequency, speed, knockbacks, recharge FROM battle_bridge WHERE cat_id = ? AND form_id = ?;", (unit_id, i))
                # [0] - HP, [1] - ATK, [2] - ATK RANGE, [3] - ATK FREQUENCY, [4] SPEED, [5] KB, [6] RECHARGE
                current_stats = list(cur.fetchone())
                current_stats[3] = frame_to_second(current_stats[3])
                stat_list.append(current_stats)
            conn.close()
            return render_template(UNIT_VIEW_HTML, names=results, form_names=form_names, rarity=rarity, talent_list=talent_list, skill_list=skill_list, stat_list=stat_list,
                                type_list=type_list, experience=results[4], costs=cat_costs, trueform_mats=trueform_materials, trueform_experience=trueform_experience, image_names=image_names)
        except Exception as e:
            abort(404, e)
    else:
        abort(404, "Unit does not exist!")


@app.route('/search', methods=['GET', 'POST'])
def unit_search():
    try:
        # Gets user's input from the unit searchbar and checks if the data received is POST or GET
        if request.method == "POST":
            search_text = request.form.get("search_text")
        else:
            search_text = request.args.get("search_text")
        # Adding %'s beforehand so it doesn't break the query
        search_text = f"%{search_text}%"
        conn, cur = connect_database(DATABASE_FILE)
        # Will check if search_text is in any of the names (e.g search_text=apple) -> (results = 'Apple Cat')
        cur.execute("SELECT cat_id, cat_first FROM battle_cat WHERE cat_first LIKE ? ORDER BY cat_first ASC;", (search_text,))
        results = cur.fetchall()
        conn.close()
        if results:
            # Removes banned characters that File Explorer does not accept
            for count, i in enumerate(results):
                i = list(i)
                i.insert(2, remove_characters(banned_characters, i[1]))
                results[count] = i
        return render_template(UNITS_HTML, results=results)
    except Exception as e:
        abort(404, e)


# Starts application
if __name__ == '__main__':
    app.run(debug=True)
