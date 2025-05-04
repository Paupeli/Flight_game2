from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/pause_menu", methods=["GET"]) #näiden pitäis viedä oikeille sivuille
def pause_menu():
    return render_template("pause_menu.html")
@app.route("/rules", methods=["GET"])
def rules():
    return render_template("rules.html")
@app.route("/scoreboard", methods=["GET"])
def scoreboard():
    return render_template("scoreboard.html")
@app.route("/main_menu", methods=["GET"])
def main_menu():
    return render_template("main_menu.html")
@app.route("/start", methods=["GET"])
def start():
    return render_template("start.html")

#@app.route("/game", methods=["GET"])
#def game():
   #return render_template("game.html") ###tää vie takasin peliin sit ku se on siinä kunnossa et sen voi yhdistää:D

@app.route("/pause", methods=["POST"]) ##itse logiikka millä pause menu toimii
def pause_logic():
    data = request.json
    pause_option = data.get("option", "").lower()

    if not pause_option:
        return jsonify({
            "message": "Game Paused",
            "options": ["Main Menu", "Continue", "Check Scoreboard", "Rules", "Quit"]
        })

    if pause_option == "continue":
        return jsonify({"status": "redirect", "location": "/game"})
    elif pause_option in ["check scoreboard", "scoreboard"]:
        return jsonify({"status": "scoreboard", "data": "Displaying Scoreboard when paused"})
    elif pause_option == "rules":
        return jsonify({"status": "redirect", "location": "/rules"})
    elif pause_option == "main menu":
        return jsonify({"status": "redirect", "location": "/main_menu"})
    elif pause_option == "quit":
        return jsonify({"status": "redirect", "location": "/start"})
    else:
        return jsonify({"error": "Invalid option"}), 400 #error handling tässä

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)