
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

flight_game_backend_app_OUTI = Flask(__name__, template_folder='Python/templates')

@flight_game_backend_app_OUTI.route("/new_game")
def new_game():
    return render_template("new_game.html")

@flight_game_backend_app_OUTI.route('/old_user')
def old_users_fetch():
    sql = f"select screen_name from game;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    users_list = []                     #TÄMÄ FOR-LOOP, KOSKA TULEE MUUTEN TUPLENA > vaikea käsitellä > muunnetaan listaksi
    for user in users:
        users_list.append(user)
    return json.dumps(users_list)           #muutettu jsonify > json dumps

def create_new_user():
    new_user = requests.form['new_screen_name']                                              #ottaa inputin frontista
    #hakee
    pass                                                                      #front-endiin printti! >> OMAT NAPIT OLEMASSA OLEVILLE >> get seuraavaan?

@flight_game_backend_app_OUTI.route('/old_user/<user>')
def get_user(user):
    sql = f"select * from game where screen_name = '{user}';"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    user_full_info = cursor.fetchall()
    cursor.close()
    if user:
        return jsonify(user_full_info)
    if not user:
        pass #404


if __name__ == '__main__':
    flight_game_backend_app_OUTI.run(use_reloader=True, host='127.0.0.1', port=3000)

