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
tasklist = []
questionsheets = []
total_points = 0
wrong_answers = 0
points = 0
#samat vanhat listat ja pistehommelit kuin vanhassakin


flight_game_backend_app = Flask(__name__)
@flight_game_backend_app.route('/flight_game/<length>')
def backend(length):
    try:
        if length > 15:
            raise ValueError

        tilakoodi = 200

        def mult_calc(length):
            length=int(length)
            if length > 10:
                a = length-10
                b = a/10
                mult = 1-b
            elif length < 10:
                a = length - 10
                b = a / 10
                mult = 1 + b
            elif length == 10:
                mult = 1
            return mult

        def routecreator(length):
            pituus = int(length)
            tehdyt = 0
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
                        if row[1] not in country_list:
                            airport_list.append(row[0])
                            country_list.append(row[1])
                            tehdyt = tehdyt + 1
            return airport_list, country_list

        def wrong_country_selector(length):
            tehdyt = 0
            needed = int(length) * 1.5
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
                            tehdyt = tehdyt + 1
            return wrong_country_list
        def question_sheet_creator(length):
            count = 0
            class Questionsheet:
                def __init__(self, clue, A, B, C, correct_answer):
                    self.clue = clue
                    self.A = A
                    self.B = B
                    self.C = C
                    self.correct_answer = correct_answer
            while length > count:
                while True:
                    num1 = random.randint(1, len(wrong_country_list))
                    num2 = random.randint(1, len(wrong_country_list))
                    num3 = random.randint(1, len(country_list))
                    country1 = wrong_country_list[num1 - 1]
                    country2 = wrong_country_list[num2 - 1]
                    country3 = country_list[num3 - 1]
                    selection_list = [country1, country2, country3]
                    if country1 not in done_country_list and country2 not in done_country_list and country3 not in done_country_list:
                        break
                while True:
                    snum1 = random.randint(1, len(selection_list))
                    snum2 = random.randint(1, len(selection_list))
                    snum3 = random.randint(1, len(selection_list))
                    if snum1 != snum2 and snum1 != snum3 and snum2 != snum3:
                        break
                A = selection_list[snum1 - 1]
                B = selection_list[snum2 - 1]
                C = selection_list[snum3 - 1]
                sql = f"select clue from clues where iso_country in (select iso_country from country where name = '{country3}') ORDER BY RAND() LIMIT 1;"
                cursor = yhteys.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    clue = row[0]
                if cursor.rowcount == 0:
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
                questionsheet = Questionsheet(clue, A, B, C, correct_answer_position)
                questionsheets.append(questionsheet)
                count = count+1
            return questionsheets
        def get_tasks(length):
            count = 0
            class Task:
                def __init__(self, task, a, b, c, answer):
                    self.task = task
                    self.a = a
                    self.b = b
                    self.c = c
                    self.answer = answer
            while count < length:
                try:
                    cursor = yhteys.cursor(dictionary=True)
                    sql = f"SELECT task, option_a, option_b, option_c, answer FROM tasks where iso_country in(select iso_country from country where name = '{country3}') ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)

                    result = cursor.fetchone()

                    if result:
                        task = result['task']
                        option_a = result['option_a']
                        option_b = result['option_b']
                        option_c = result['option_c']
                        correct_answer = result['answer']
                        mission = Task(task, option_a, option_b, option_c, correct_answer)
                        tasklist.append(mission)
                        count = count+1
                    else:
                        return None
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            return tasklist
        mult_calc(length)
        routecreator(length)
        wrong_country_selector(length)
        question_sheet_creator(length)
        response = {
            "countries": country_list,
            "airports": airport_list,
            "wrong countries": wrong_country_list,
            "questionsheets": questionsheets,
            "Tasks": tasklist
        }
    except ValueError:
        tilakoodi = 400
        response = {
                "status": tilakoodi,
                "teksti": "Virheellinen luku"
            }
    jsonvast = json.dumps(response)
    return Response(response=jsonvast, status=tilakoodi, mimetype="application/json")
