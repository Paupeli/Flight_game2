from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='flight_game',
    user='keltanokat',
    password='lentopeli',
    autocommit=True,
    collation='utf8mb3_general_ci'
)

@app.route("/flight_game/scoreboard")
#Luodaan sanakirja sql:n palauttamista arvoista
#Arvot ovat sanakirjassa valmiiksi järjestyksessä, koska sql-kysely järjestää ne! Ei tarvetta sorttailla
def scoreboard():
    sql = f"select screen_name, high_score from game where high_score != 0 order by high_score desc limit 5;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return_data = []
    for row in result:
        screen_name = row[0] if row[0] is not None else "N/A"
        high_score = row[1] if row[1] is not None else "N/A"
        return_data.append({"screen_name" : screen_name , "high_score" : high_score})
    return jsonify(return_data)

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=2192) #pyörittää apin