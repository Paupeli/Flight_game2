from flask import Flask, request, jsonify, render_template, redirect

app= Flask (__name__)

@app.route("/main_menu")
def another_main_menu():
    return render_template("main_menu.html")  #vie takasin main menuun

@app.route("/scoreboard")
def another_scoreboard_html():
    return render_template('scoreboard.html')  #vie scoreboardiin

@app.route("/rules")
def another_rules():
    return render_template("rules.html")  #vie rulesiin

@app.route("/quit")
def quit_game():
    return render_template("start.html") #vie takas alotussivulle

@app.route("/")
def pause_menu():
    return render_template("pause_menu.html")

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)