
from flask import Flask, jsonify, render_template, Response, redirect, request
from flask_cors import CORS
import json
import mysql.connector
import random
import jsonpickle

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




#samat vanhat listat ja pistehommelit kuin vanhassakin

# MAIN MENU

@app.route("/")
def start(): #tässä aloitussivu
    return render_template("start.html")

@app.route("/start")
def go_to_start(): #quitistä takaisin aloitukseen
    return render_template("start.html")

@app.route("/rules")
def rules(): #tästä instructions/rulesiin
    return render_template("rules.html")

@app.route("/main_menu")
def main_menu(): #tästä mennää takasin aloitussivulle
    return render_template("main_menu.html")                    #MYÖS pause linkittyy tähän

#PAUSE MENU

@app.route("/scoreboard")
def pause_scoreboard_html():
    return render_template('scoreboard.html')  #vie scoreboardiin

@app.route("/rules")
def pause_rules():
    return render_template("rules.html")  #vie rulesiin

@app.route("/quit")
def quit_game():
    return redirect('/') #vie takas alotussivulle

#PAUSE MENU LOPPUU TÄHÄN!!

#SCOREBOARD:

@app.route("/scoreboard")
def scoreboard():
    return render_template('scoreboard.html')

@app.route("/flight_game/scoreboard")
#Luodaan sanakirja sql:n palauttamista arvoista
#Arvot ovat sanakirjassa valmiiksi järjestyksessä, koska sql-kysely järjestää ne! Ei tarvetta sorttailla
def scoreboard_json():
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

@app.route("/flight_game/scoreboard/save_score/<user>", methods=['POST'])
def save_score(user):
    new_high_score = False
    data = request.get_json()
    score = data.get('score')
    sql1 = f"select high_score from game where screen_name = '{user}';"
    cursor = yhteys.cursor()
    cursor.execute(sql1)
    high_score = cursor.fetchone()
    if high_score is None or high_score[0] is None:
        new_high_score = True
        sql2 = f"update game set high_score = {score} where screen_name = '{user}';"
        cursor.execute(sql2)
        yhteys.commit()
        cursor.close()
    elif high_score[0] < score:
        new_high_score = True
        sql2 = f"update game set high_score = {score} where screen_name = '{user}';"
        cursor.execute(sql2)
        yhteys.commit()
        cursor.close()
    else: new_high_score = False
    return jsonify({"new_high_score": new_high_score})                                                             #Tarkistetaan toimiiko true/false

# HAHMON VALINTA JA LUONTI:

@app.route("/new_game")
#tämä avaa new game -valikon (url)
def new_game():
    return render_template("new_game.html")

@app.route("/new_game/old_user")
def old_user():
    return render_template("old_user.html")

@app.route('/new_game/old_user/fetch')
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
    return jsonify(users_list)                                               # !!!! DROP DOWN VALIKKO >> LINKKI /old_user/<user> >> uuden käyttäjän valinta ?

@app.route('/new_game/old_user/<username>')
# tämä palauttaa arvon muuttujalle user > käytetään myöhemmin tallennettaessa pisteitä, jne
def get_user(username):
    sql = f"select screen_name from game where screen_name = '{username}';"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return jsonify({"error": "Not found", "code": 404}), 404
    user = result[0]
    return jsonify({'username': user})          # !!!!!!!!!!! LINKATAAN USER-valinta frontissa SUORAAN PELIN JAVASCRIPTIIN !!!!!!!!!!!!!!!!!
                                            # ELI tämä vain päivittää user-arvon bäkkärille mutta ei palauta mitään :)

@app.route("/new_game/new_user/<username>", methods=['GET'])
# tämä luo ja tallentaa käyttäjän JA palauttaa arvon muuttujalle user > käytetään myöhemmin tallennettaessa pisteitä, jne
# !!!! TÄHÄN tarvitaan "username" -tieto API:sta !!!!
def create_new_user(username):
    #Huom, sql-injektion esto puuttuu :D
    try:
        user = username
        sql = f"select screen_name from game where screen_name = '{user}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            return jsonify({"error": "Username already exists"}), 400

        # Tehdään uusi id !
        new_id = "SELECT COALESCE(MAX(id), 0) + 1 FROM game;"
        cursor.execute(new_id)
        next_id = cursor.fetchone()[0]

        # tungetaan käyttäjä sql:ään
        sql2 = f"INSERT INTO game (id, location, screen_name, score, high_score) VALUES ('{next_id}', 'EFHK', '{user}', 0, 0);"
        cursor.execute(sql2)
        yhteys.commit()
        cursor.close()
        return jsonify({'username': user})
    except Exception as e:
        return jsonify({"error": str(e)}), 500                      #Palauttaa arvon "user", mutta onko tällä käyttöä frontissa? Tärkeää sql-kyselyissä.

@app.route("/new_game/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/new_game/questionsheet")
def questions():
    return render_template("questionsheet.html")

# HAHMONLUONTI PÄÄTTYY TÄHÄN:

# PELIN LOPETUS:
@app.route("/new_game/finish")
def finish():
    return render_template("finish.html")

# REITIN PITUUDEN VALINTA TÄHÄN:

@app.route('/new_game/pick_length')
def pick_length():
    return render_template('pick_length.html')                        #SYÖTETÄÄN 'lenght' arvo (5, 10, 15) Ronin koodille

@app.route('/createroute/<length>')
def backend(length): #pääfunktio (joka on vaa funktio, joka toteuttaa 5 funktioita :D)
    try:
        country_list = []
        airport_list = []
        wrong_country_list = []
        done_country_list = []
        tasklist = []
        questionsheets = []
        length = int(length)
        if length > 15 or length <= 0:
            raise ValueError #jos pituus on yli 15, nolla tai nollaa pienempi tekee ValueErrorin, joka pysäyttää koodin
        tilakoodi = 200

        def mult_calc(length): #laskee pistekertoimen
            length=int(length) #muuttaa length:in integeriksi, jotta sitä voi verrata numeroihin
            if length > 10:
                a = length-10
                b = a/10
                mult = 1-b #esim. reitinpituus = 15. 15-10=5, 5/10=0.5, 1-0,5 = 0,5, kerroin siis 0,5
            elif length < 10:
                a = 10-length
                b = a / 10
                mult = 1 + b #esim. reitinpituus = 5, 10-5=5, 5/10=0.5, 1+0.5=1.5, kerroin siis 1,5
            else:
                mult = 1 #jos reitin pituus on 10, kerroin yhdessä
            return mult

        def routecreator(length): #tekee reitin
            pituus = int(length)
            tehdyt = 0 #while loopin toistojen laskemiseksi
            while tehdyt < pituus:  # looppaa niin kauan kunnes lentokenttiä on reitinpituuden verran
                num = random.randint(1, 261)
                sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                while cursor.rowcount == 0:  # jos ei saa lentokenttää ekalla sql-komennolla, kokeilee sitä uudelleen
                    num = random.randint(1, 261)
                    sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                    cursor = yhteys.cursor()
                    cursor.execute(sql)
                    result = cursor.fetchall()
                else:
                    for row in result:
                        if row[1] not in country_list: #lisää lentokentät ja maat listoihin
                            airport_list.append(row[0])
                            country_list.append(row[1])
                            tehdyt = tehdyt + 1
            return airport_list, country_list #palauttaa listat json:oitavaksi :D

        def wrong_country_selector(length): #valitsee väärät maat kysymyksiä varten
            tehdyt = 0 #while loopin toistojen laskemiseksi
            needed = int(length) * 1.5 #monta toistoa tarvitsee tehdä, että saadaan haluttu määrä vääriä maita
            while tehdyt < needed:
                num = random.randint(1, 130)
                sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                while cursor.rowcount == 0: #toistaa sql-komentoa, mikäli SQL:stä ei saa mitään ekalla kerralla
                    num = random.randint(1, 130)
                    sql = f"select airport.name, country.name from airport inner join country on airport.iso_country = country.iso_country and airport.id = {num} order by rand();"
                    cursor = yhteys.cursor()
                    cursor.execute(sql)
                    result = cursor.fetchall()
                else:
                    for row in result:
                        if row[1] not in country_list and row[1] not in wrong_country_list:
                            wrong_country_list.append(row[1]) #lisää maan väärien maiden listaan ja lisää yhden toiston laskuriin
                            tehdyt = tehdyt + 1
            return wrong_country_list

        def question_sheet_creator(length): #luo kysymyslomakkeet
            count = 0 #while loopin toistojen laskemiseksi
            class Questionsheet: #kysymyslomakkeiden luokka, sisältää vihjeen, mahdolliset vastaukset ja oikean vastauksen
                def __init__(self, clue, A, B, C, correct_answer):
                    self.clu = clue
                    self.A = A
                    self.B = B
                    self.C = C
                    self.correct_answer = correct_answer
            while length > count: #toistaa looppia kunnes laskuri on samassa reitin pituuden kanssa
                while True:
                    num1 = random.randint(1, len(wrong_country_list))
                    num2 = random.randint(1, len(wrong_country_list))
                    num3 = random.randint(1, len(country_list))
                    #numerot ovat seuraavaa koodia varten. Num3 määräytyy oikeiden maiden perusteella. 1 & 2 taas väärien.
                    country1 = wrong_country_list[num1 - 1]
                    country2 = wrong_country_list[num2 - 1]
                    country3 = country_list[num3 - 1]
                    selection_list = [country1, country2, country3]
                    #luo edellisten numeroiden perusteella listan maista, käyttäen edellämainittuja numeroita
                    if country1 not in done_country_list and country2 not in done_country_list and country3 not in done_country_list:
                        break #looppi toteutuu niin pitkään kunnes mikään maista ei ole listassa, jossa on maat, jotka seuraava funktio käy läpi.
                while True:
                    snum1 = random.randint(1, len(selection_list))
                    snum2 = random.randint(1, len(selection_list))
                    snum3 = random.randint(1, len(selection_list)) #luo numerot sitä varten, että mikä maa on mikäkin vastaus
                    if snum1 != snum2 and snum1 != snum3 and snum2 != snum3: #varmistaa etteivät numerot ole samoja
                        break
                A = selection_list[snum1 - 1]
                B = selection_list[snum2 - 1]
                C = selection_list[snum3 - 1]
                #valitsee mikä maa on mikäkin vaihtoehto
                sql = f"select clue from clues where iso_country in (select iso_country from country where name = '{country3}') ORDER BY RAND() LIMIT 1;"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                #sql-komento, joka valitsee yhden vihjeen sille maalle, joka valittiin oikeaksi maaksi
                for row in result:
                    clue = row[0]
                while cursor.rowcount == 0: #toistaa edellisen loopin, mikäli vihjettä ei löydy
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
                #laittaa maille vastaavat vastausvaihtoehdot luettavaan muoton
                questionsheet = Questionsheet(clue, A, B, C, correct_answer_position) #luo Questionsheet luokkaa hyödyntäen kysymyslomakkeen, johon sisältyy vihje, vastausvaihtoehdot ja oikea vastaus
                jsonquestionsheet = jsonpickle.encode(questionsheet) #tekee edellisestä kysymyslomakkeesta json:ille luettavan version
                questionsheets.append(jsonquestionsheet) #lisää kysymyslomakkeen kysymyslomakelistaan
                count = count+1 #nostaa laskuria
            return questionsheets

        def get_tasks(length): #ottaa tehtävät
            count = 0 #while loopin toistojen laskemiseksi
            class Task: #samankaltainen luokka kuin edellisessäkin funktiossa
                def __init__(self, task, a, b, c, answer):
                    self.task = task
                    self.a = a
                    self.b = b
                    self.c = c
                    self.answer = answer

            while count < length:
                while True:
                    num = random.randint(0, length-1) #nämä luvut siksi että listat ovat hassuja olioita
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
                    #Pauliinan koodia edellisestä peliversiosta, varmaan selkämpää kuin mun :D

                    if result:
                        task = result['task']
                        option_a = result['option_a']
                        option_b = result['option_b']
                        option_c = result['option_c']
                        correct_answer = result['answer']
                        mission = Task(task, option_a, option_b, option_c, correct_answer)
                        jsonmission = jsonpickle.encode(mission)
                        tasklist.append(jsonmission)
                        count = count+1 #sama idea kuin edellisessäkin funktiossa
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
        #pyöräyttää edelliset funktiot parametreinään reitin pituus
        response = {
            "countries": country_list,
            "airports": airport_list,
            "wrong countries": wrong_country_list,
            "questionsheets": questionsheets,
            "Tasks": tasklist,
            "Mult": mult
        } #funktioiden palauttamat arvot json-muodossa

    except ValueError: #virheenkäsittelyä, mikäli reitti on liian pitkä tai lyhyt
        tilakoodi = 400
        response = {
                "status": tilakoodi,
                "teksti": "Virheellinen luku"
            }
    jsonvast = json.dumps(response)
    return Response(response=jsonvast, status=tilakoodi, mimetype="application/json")


#@flight_game_backend_app.errorhandler(404) #virheenhallintaa, mikäli sivua ei löydy
#def page_not_found(virhekoodi):
    #vastaus = {
        #"status" : "404",
        #"teksti" : "Virheellinen päätepiste"
    #}
    #jsonvast = json.dumps(vastaus)
    #return Response(response=jsonvast, status=404, mimetype="application/json")

@app.errorhandler(404)  # error handling
def page_not_found(error):
    return jsonify({"error": "Not found", "code": 404}), 404

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000) #pyörittää apin
