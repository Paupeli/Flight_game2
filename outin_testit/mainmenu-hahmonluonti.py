
import mysql.connector
from flask import Flask, Response, jsonify, render_template
import requests
import json
import jsonpickle

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='flight_game',
    user='keltanokat',
    password='lentopeli',
    autocommit=True,
    collation='utf8mb3_general_ci'
)

flight_game_backend_app = Flask(__name__, template_folder='Python/templates')

# HAHMON VALINTA JA LUONTI:

@app.route("/new_game")
#tämä avaa new game -valikon (url)
def new_game():
    return render_template("new_game.html")

@app.route('/old_user')
# tämä palauttaa listan vanhoista käyttäjistä valikkoa varten
def old_users_fetch():
    sql = f"select screen_name from game;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    users_list = []
    for user in users:
        users_list.append(user[0])
    return json.dumps(users_list)                                               # !!!! DROP DOWN VALIKKO >> LINKKI /old_user/<user> >> uuden käyttäjän valinta ?

@app.route('/old_user/<user>')
# tämä palauttaa arvon muuttujalle user > käytetään myöhemmin tallennettaessa pisteitä, jne
def get_user(user):
    user = user
    sql = f"select * from game where screen_name = '{user}';"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    user_full_info = cursor.fetchall()
    cursor.close()
    if not user:
        pass #404
    if user:
        return json.dumps(user)

@app.route("/new_user")
# tämä luo ja tallentaa käyttäjän JA palauttaa arvon muuttujalle user > käytetään myöhemmin tallennettaessa pisteitä, jne
def create_new_user():
    user = requests.get.form("new_screen_name").text                                # !!!! TÄHÄN tarvitaan "new_screen_name" -tieto API:sta !!!!

    sql = f"select * from game where screen_name = '{user}';"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:
        pass #404
    else:
        sql2 = f"update game set location = (select ident from airport where ident = 'EFHK') where screen_name = '{user}';"
        cursor.execute(sql2)
        yhteys.commit()
        cursor.close()
        return json.dumps(user)

# HAHMONLUONTI PÄÄTTYY TÄHÄN


if __name__ == '__main__':
    flight_game_backend_app.run(use_reloader=True, host='127.0.0.1', port=3000)

