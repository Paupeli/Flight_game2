from flask import Flask, Response
import json
import mysql.connector
import random
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='flight_game',
    user='keltanokat',
    password='lentopeli',
    autocommit=True,
    collation='utf8mb3_general_ci'
)
country_list = []
airport_list = []
wrong_country_list = []
done_country_list = []
cluelist = []
count = 0
total_points = 0
wrong_answers = 0
points = 0
#samat vanhat listat ja pistehommelit kuin vanhassakin
maavalitsin_app = Flask(__name__)
#pituus*1.5
@maavalitsin_app.route('/maavalitsin/<length>')
def country_selector(length):
    try:
        tilakoodi = 200
        tehdyt = 0
        needed = int(length)*1.5
        while tehdyt < needed:
            num = random.randint(1, 130)
            sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
            cursor = yhteys.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            while cursor.rowcount == 0:
                num = random.randint(1, 130)
                sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
            else:
                for row in result:
                    if row[1] not in country_list and row[1] not in wrong_country_list:
                        wrong_country_list.append(row[1])
                        tehdyt = tehdyt+1
        response = {
            "countries": wrong_country_list
        }
    except ValueError:
        tilakoodi = 400
        response = {
            "status": tilakoodi,
            "teksti": "Virheellinen reitinpituus"
        }
    jsonresponse = json.dumps(response)  # muuttaa vastauksen virallisesti json-muotoon, jotta javascript voi lukea sitä
    return Response(response=jsonresponse, status=tilakoodi, mimetype="application/json")  # palauttaa vastauksen, apin tilan ja en tiedä mitä vika tekee mutta se tarvitaan :D
@maavalitsin_app.errorhandler(404)
def page_not_found(virhekoodi):
    vastaus = {
        "status" : "404",
        "teksti" : "Virheellinen päätepiste"
    }
    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, status=404, mimetype="application/json")
if __name__ == '__main__':
    maavalitsin_app.run(use_reloader=True, host='127.0.0.1', port=3000)


