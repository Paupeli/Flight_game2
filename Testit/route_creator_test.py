from formatter import NullWriter

from flask import Flask, jsonify, render_template, Response, redirect, request
from flask_cors import CORS
import json
import mysql.connector
import random
import jsonpickle
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#tää pyörii nyt http://127.0.0.1:3000/
#html tiedostot on templates kansiossa
#js tiedostot kuvat yms yms static kansiossa

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
tasklist = []
questionsheets = []

@app.route('/createroute/<length>')
def backend(length):  # pääfunktio (joka on vaa funktio, joka toteuttaa 5 funktioita :D)
    try:
        length = int(length)
        if length > 15 or length <= 0:
            raise ValueError  # jos pituus on yli 15, nolla tai nollaa pienempi tekee ValueErrorin, joka pysäyttää koodin
        tilakoodi = 200

        def mult_calc(length):  # laskee pistekertoimen
            length = int(length)  # muuttaa length:in integeriksi, jotta sitä voi verrata numeroihin
            if length > 10:
                a = length - 10
                b = a / 10
                mult = 1 - b  # esim. reitinpituus = 15. 15-10=5, 5/10=0.5, 1-0,5 = 0,5, kerroin siis 0,5
            elif length < 10:
                a = 10 - length
                b = a / 10
                mult = 1 + b  # esim. reitinpituus = 5, 10-5=5, 5/10=0.5, 1+0.5=1.5, kerroin siis 1,5
            else:
                mult = 1  # jos reitin pituus on 10, kerroin yhdessä
            return mult

        def routecreator(length):  # tekee reitin
            pituus = int(length)
            tehdyt = 0  # while loopin toistojen laskemiseksi
            yritykset1 = 0
            while tehdyt < pituus and yritykset1 < 1000:  # looppaa niin kauan kunnes lentokenttiä on reitinpituuden verran
                num = random.randint(1, 43)
                sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                yritykset1 += 1
                while cursor.rowcount == 0:  # jos ei saa lentokenttää ekalla sql-komennolla, kokeilee sitä uudelleen
                    num = random.randint(1, 43)
                    sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                    cursor = yhteys.cursor()
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    yritykset1 += 1
                else:
                    for row in result:
                        if row[1] not in country_list:  # lisää lentokentät ja maat listoihin
                            airport_list.append(row[0])
                            country_list.append(row[1])
            return  # palauttaa listat json:oitavaksi :D

        def wrong_country_selector(length):  # valitsee väärät maat kysymyksiä varten
            tehdyt = 0  # while loopin toistojen laskemiseksi
            needed = int(length) * 1.5  # monta toistoa tarvitsee tehdä, että saadaan haluttu määrä vääriä maita
            while tehdyt < needed:
                num = random.randint(1, 43)
                sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                while cursor.rowcount == 0:  # toistaa sql-komentoa, mikäli SQL:stä ei saa mitään ekalla kerralla
                    num = random.randint(1, 43)
                    sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                    cursor = yhteys.cursor()
                    cursor.execute(sql)
                    result = cursor.fetchall()
                else:
                    for row in result:
                        if row[1] not in country_list and row[1] not in wrong_country_list:
                            wrong_country_list.append(
                                row[1])  # lisää maan väärien maiden listaan ja lisää yhden toiston laskuriin
            return wrong_country_list

        def question_sheet_creator(length):  # luo kysymyslomakkeet
            count = 0  # while loopin toistojen laskemiseksi

            class Questionsheet:  # kysymyslomakkeiden luokka, sisältää vihjeen, mahdolliset vastaukset ja oikean vastauksen
                def __init__(self, clue, a, b, c, answer):
                    self.clue = clue
                    self.a = a
                    self.b = b
                    self.c = c
                    self.answer = answer

            while length > count:  # toistaa looppia kunnes laskuri on samassa reitin pituuden kanssa
                while True:
                    num1 = random.randint(1, len(wrong_country_list))
                    num2 = random.randint(1, len(wrong_country_list))
                    num3 = random.randint(1, len(country_list))
                    # numerot ovat seuraavaa koodia varten. Num3 määräytyy oikeiden maiden perusteella. 1 & 2 taas väärien.
                    country1 = wrong_country_list[num1 - 1]
                    country2 = wrong_country_list[num2 - 1]
                    country3 = country_list[num3 - 1]
                    selection_list = [country1, country2, country3]
                    # luo edellisten numeroiden perusteella listan maista, käyttäen edellämainittuja numeroita
                    if country1 not in done_country_list and country2 not in done_country_list and country3 not in done_country_list:
                        break  # looppi toteutuu niin pitkään kunnes mikään maista ei ole listassa, jossa on maat, jotka seuraava funktio käy läpi.
                while True:
                    snum1 = random.randint(1, len(selection_list))
                    snum2 = random.randint(1, len(selection_list))
                    snum3 = random.randint(1,
                                           len(selection_list))  # luo numerot sitä varten, että mikä maa on mikäkin vastaus
                    if snum1 != snum2 and snum1 != snum3 and snum2 != snum3:  # varmistaa etteivät numerot ole samoja
                        break
                A = selection_list[snum1 - 1]
                B = selection_list[snum2 - 1]
                C = selection_list[snum3 - 1]
                # valitsee mikä maa on mikäkin vaihtoehto
                sql = f"select clue from clues where iso_country in (select iso_country from country where name = '{country3}') ORDER BY RAND() LIMIT 1;"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                # sql-komento, joka valitsee yhden vihjeen sille maalle, joka valittiin oikeaksi maaksi
                for row in result:
                    clue = row[0]
                while cursor.rowcount == 0:  # toistaa edellisen loopin, mikäli vihjettä ei löydy
                    sql = f"select clue from clues where iso_country in (select iso_country from country where name = '{country3}') ORDER BY RAND() LIMIT 1;"
                    cursor = yhteys.cursor()
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for row in result:
                        clue = row[0]
                correct_answer_position = ''
                if country3 == A:
                    correct_answer_position = 'A'
                elif country3 == B:
                    correct_answer_position = 'B'
                elif country3 == C:
                    correct_answer_position = 'C'
                # laittaa maille vastaavat vastausvaihtoehdot luettavaan muoton
                questionsheet = Questionsheet(clue, A, B, C,
                                              correct_answer_position)  # luo Questionsheet luokkaa hyödyntäen kysymyslomakkeen, johon sisältyy vihje, vastausvaihtoehdot ja oikea vastaus
                jsonquestionsheet = jsonpickle.encode(
                    questionsheet)  # tekee edellisestä kysymyslomakkeesta json:ille luettavan version
                questionsheets.append(jsonquestionsheet)  # lisää kysymyslomakkeen kysymyslomakelistaan
                count = count + 1  # nostaa laskuria
            return questionsheets

        def get_tasks(length):  # ottaa tehtävät
            count = 0  # while loopin toistojen laskemiseksi

            class Task:  # samankaltainen luokka kuin edellisessäkin funktiossa
                def __init__(self, task, a, b, c, answer):
                    self.task = task
                    self.a = a
                    self.b = b
                    self.c = c
                    self.answer = answer

            while count < length:
                while True:
                    num = random.randint(0, length - 1)  # nämä luvut siksi että listat ovat hassuja olioita
                    num = int(num)
                    country = country_list[num]
                    if country not in done_country_list:
                        country3 = country
                        done_country_list.append(country)
                        break
                try:
                    cursor = yhteys.cursor(dictionary=True)
                    sql = f"SELECT task, option_a, option_b, option_c, answer FROM tasks where iso_country in(select iso_country from country where name = '{country3}') ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    # Pauliinan koodia edellisestä peliversiosta, varmaan selkämpää kuin mun :D

                    if result:
                        task = result['task']
                        option_a = result['option_a']
                        option_b = result['option_b']
                        option_c = result['option_c']
                        correct_answer = result['answer']
                        mission = Task(task, option_a, option_b, option_c, correct_answer)
                        jsonmission = jsonpickle.encode(mission)
                        tasklist.append(jsonmission)
                        count = count + 1  # sama idea kuin edellisessäkin funktiossa
                    else:
                        return None
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            return tasklist

        mult = mult_calc(length)
        routecreator(length)
        wrong_country_selector(length)
        question_sheet_creator(length)
        get_tasks(length)

        # pyöräyttää edelliset funktiot parametreinään reitin pituus
        response = {

            "countries": country_list,
            "airports": airport_list,
            "wrong countries": wrong_country_list,
            "questionsheets": questionsheets,
            "Tasks": tasklist,
            "Mult": mult

        }  # funktioiden palauttamat arvot json-muodossa

    except ValueError:  # virheenkäsittelyä, mikäli reitti on liian pitkä tai lyhyt
        tilakoodi = 400
        response = {
            "status": tilakoodi,
            "teksti": "Virheellinen luku"
        }
    jsonvast = json.dumps(response)
    return Response(response=jsonvast, status=tilakoodi, mimetype="application/json")

@app.errorhandler(404)  # error handling
def page_not_found(error):
    return jsonify({"error": "Not found", "code": 404}), 404

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000) #pyörittää apin