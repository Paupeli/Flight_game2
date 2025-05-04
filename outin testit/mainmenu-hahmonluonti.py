import mysql.connector
from flask import Flask, Response, jsonify

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='flight_game',
    user='keltanokat',
    password='lentopeli',
    autocommit=True,
    collation='utf8mb3_general_ci'
)

flight_game_backend_app = Flask(__name__)

@flight_game_backend_app.route('/old_user')
def old_users_fetch():
    users_sql = f"select screen_name from game;"
    cursor = yhteys.cursor()
    cursor.execute(users_sql)
    users = cursor.fetchall()
    return jsonify(users)
    #front-endiin printti! >> OMAT NAPIT OLEMASSA OLEVILLE
def select_old_user():



if __name__ == '__main__':
    flight_game_backend_app.run(use_reloader=True, host='127.0.0.1', port=3000)




#    global option
#    global user
#
 #   while True:
  #      #Looppaa main menuun kunnes pelaaja haluaa alottaa uuden pelin
   #     print("-------------------------\n")
    #    print(f"\n>New Game\n>Scoreboard\n>Rules\n>Quit\n")
     #   option = input("Please select >").lower()
      #  if option == "new game" or option == "new":
       #     user = new_game()
        #    break
        #elif option == "scoreboard":
           # scoreboard()
        #elif option == "rules":
     #       instructions()
      #  elif option == "quit":
       #     quit()
   # return user

