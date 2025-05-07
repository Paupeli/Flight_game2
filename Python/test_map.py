from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='keltanokat',
    password='lentopeli',
    autocommit=True,
    collation='utf8mb3_general_ci'
)

@app.route("/")
def index():
    return render_template("map.html")  #kartta html

@app.route("/flight_path")
def flight_path():
    cursor = yhteys.cursor(dictionary=True)


    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE ident = 'EFHK'")
    helsinki = cursor.fetchone()


    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE ident = 'LOWW'")
    vienna = cursor.fetchone()

    cursor.close()

    if helsinki and vienna:
        return jsonify({
            "start": {"lat": helsinki["latitude_deg"], "lng": helsinki["longitude_deg"]},
            "end": {"lat": vienna["latitude_deg"], "lng": vienna["longitude_deg"]}
        })
    else:
        return jsonify({"error": "Coordinates not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=2192)