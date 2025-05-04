
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

@flight_game_backend_app.route("/new_game")
def new_game():
    return render_template("new_game.html")

@flight_game_backend_app_OUTI.route('/old_user')
def old_users_fetch():
    sql = f"select screen_name from game;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    users_list = []
    for user in users:
        users_list.append(user[0])
    return json.dumps(users_list)

@flight_game_backend_app.route('/old_user/<user>')
def get_user(user):
    sql = f"select * from game where screen_name = '{user}';"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    user_full_info = cursor.fetchall()
    cursor.close()
    if not user:
        pass #404
    if user:
        return jsonify(user_full_info)          #Ei välttämättä ole tarve palauttaa tietoa - riittää että screen_name on tallessa?

@flight_game_backend_app.route("/new_user")
def create_new_user():
    user = requests.get.form("new_screen_name").text     #TÄHÄN tarvitaan new_screen_name -tieto API:sta

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
        return json.dumps(user)                 #Ei välttämättä ole tarve palauttaa tietoa - riittää että screen_name on tallessa?


if __name__ == '__main__':
    flight_game_backend_app.run(use_reloader=True, host='127.0.0.1', port=3000)

