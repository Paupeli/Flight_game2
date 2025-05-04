from flask import Flask, jsonify, render_template

app = Flask(__name__)

#tää pyörii nyt http://127.0.0.1:5000/
#html tiedostot on Templates_OUTI kansiossa
#js tiedostot kuvat yms yms static kansiossa

@app.route("/")
def main_menu(): #tässä main menu
    return render_template("main_menu.html")

@app.route("/new_game")
def new_game():
    return render_template("new_game_OUTIN_TESTI.html")

@app.route("/rules")
def rules(): #tästä instructions/rulesiin
    return render_template("rules.html")

@app.route("/scoreboard")
def scoreboard(): #tästä scoreboardiin
    return render_template("scoreboard.html")

@app.route("/start")
def start(): #tästä mennää takasin aloitussivulle
    return render_template("start.html")

@app.errorhandler(404)  #error handling
def page_not_found(error):
    return jsonify({"error": "Not found", "code": 404}), 404

if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=5000) #apin pyöritys