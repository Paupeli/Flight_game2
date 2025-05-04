from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def pause_scoreboard ():
    return "Displaying Scoreboard when paused" ##Tästä mennään scoreboardiin

def pause_rules ():
    return "Showing Rules when paused" ##Tästä mennään rulesiin

@app.route("/pause_menu", methods=["GET"])
def pause_menu():
    return render_template("pause_menu.html")

@app.route("/pause", methods=["POST"])
def pause_logic():
    data = request.json
    pause_option = data.get("option", "").lower()

    if not pause_option:
        return jsonify({
            "message": "Game Paused",
            "options": ["Continue", "Check Scoreboard", "Rules", "Quit"]
        })

    if pause_option == "continue":
        return jsonify({"status": "resumed"})
    elif pause_option in ["check scoreboard", "scoreboard"]:
        return jsonify({"status": "scoreboard", "data": pause_scoreboard()})
    elif pause_option == "rules":
        return jsonify({"status": "rules", "data": pause_rules()})
    elif pause_option == "quit":
        return jsonify({"status": "quitting", "message": "Quitting game..."})
    else:
        return jsonify({"error": "Invalid option"}), 400 ##error handling tässä

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)