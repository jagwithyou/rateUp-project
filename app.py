from flask import Flask, render_template, request, session, redirect
from flask.wrappers import Request
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, Text
import psycopg2
import config
from flask_session import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

print("================",config.host)
con = psycopg2.connect(
        database=config.database, 
        user=config.user,
        password=config.password,
        host=config.host, 
        port=config.port
    )
print("Database opened successfully")


templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

@app.route("/", methods = ["GET", "POST"])
def home():
    if not session.get("id"):
        return redirect("/signIn")
    cur = con.cursor()
    cur.execute("select * from games")
    data = cur.fetchall()
    print(data)    
    return render_template("HomePageNew.html", data=data, session=session.get("id"))

@app.route("/Update-games", methods = ["GET", "POST"])
def update_games():
    cur = con.cursor()
    cur.execute("select * from games")
    data = cur.fetchall()
    print(data)    
    return render_template("HomePageEdit.html", data=data, session=session.get("id"))

@app.route("/home", methods = ["GET"])
def home_new():
    return render_template("HomePage.html")

@app.route("/rate-game/<int:id>", methods = ["POST", "GET"])
def rate_movie(id):
    cur = con.cursor()
    cur.execute("select * from games where id="+str(id))
    data = cur.fetchall()
    print(request.method)
    if request.method == 'POST':
        rating = request.form.get("rate")
        message = request.form.get("message")
        print(rating, message)
        cur.execute("INSERT INTO game_rating (rating, message, ratedby, gameid) VALUES(%s, %s, %s, %s);", (rating, message, id, 1))
        con.commit()
        return redirect('/')
    return render_template("RateTheMovie.html", data=data[0], session=session.get("id"))

@app.route("/uploader", methods = ["POST", "GET"])
def upload_game_details():
    if request.method == 'POST':
        f = request.files['file']
        f.save("static/Images/"+secure_filename(f.filename))
        game_name = request.form.get("game_name")
        desc = request.form.get("desc")
        filename = f.filename
        if f.filename:
            cur = con.cursor()
            print(cur.execute("INSERT INTO games (name, description, filename) VALUES(%s, %s, %s);", (game_name, desc, filename)))
            con.commit()
            cur.close()
            return redirect("/")
    elif request.method == 'GET':
        return render_template("UploadGame.html", session=session.get("id"))

@app.route("/game/<int:id>", methods = ["POST", "GET"])
def game_details(id):
    cur = con.cursor()
    cur.execute("select * from games where id="+str(id))
    data = cur.fetchall()
    print(request.method)
    if request.method == 'POST':
        f = request.files['file']
        if f:
            f.save("static/Images/"+secure_filename(f.filename))
        game_name = request.form.get("game_name")
        desc = request.form.get("desc")
        filename = f.filename if f else data[0][3]
        cur.execute("UPDATE games set name = %s, description=%s, filename=%s;", (game_name, desc, filename))
        con.commit()
        cur.execute("select * from games where id="+str(id))
        data = cur.fetchall()
        cur.close()
        return render_template("UpdateGame.html", data=data[0], session=session.get("id"))
    elif request.method == 'GET':
        return render_template("UpdateGame.html", data=data[0], session=session.get("id"))

@app.route("/game-delete/<int:id>", methods = ["POST"])
def game_delete(id):
    cur = con.cursor()
    cur.execute("DELETE FROM games WHERE id = %s;", (str(id)))
    con.commit()
    cur.close()
    return redirect("/Update-games")

@app.route("/user/<int:id>", methods = ["POST", "GET"])
def user_details(id):
    cur = con.cursor()
    cur.execute("select * from users where id="+str(id))
    data = cur.fetchall()
    print(request.method)
    if request.method == 'POST':
        name = request.form.get("user_name")
        email = request.form.get("email")
        password = request.form.get("password")
        cur.execute("UPDATE users set name = %s, email=%s, password=%s;", (name, email, password))
        con.commit()
        cur.execute("select * from users where id="+str(id))
        data = cur.fetchall()
        cur.close()
        return render_template("UpdateUser.html", data=data[0], session=session.get("id"))
    elif request.method == 'GET':
        return render_template("UpdateUser.html", data=data[0], session=session.get("id"))

@app.route("/user-delete/<int:id>", methods = ["POST"])
def user_delete(id):
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (str(id)))
    con.commit()
    cur.close()
    return redirect("/")




@app.route("/signUp", methods = ["GET", "POST"])
def signUp():
    name = request.args.get("name")
    email = request.args.get("email")
    password = request.args.get("password")
    if (name): 
        cur = con.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES(%s, %s, %s);", (name, email, password))
        con.commit()
        cur.close()
        return redirect("/signIn")
    return render_template("SignUp.html")

@app.route("/signIn", methods = ["GET", "POST"])
def signIn():
    email = request.args.get("email")
    password = request.args.get("password")
    if (email):
        cur = con.cursor()
        cur.execute("select * from users")
        users = cur.fetchall()
        for user in users:
            print(user)
            print(email, password)
            if user[2] == email and user[3] == password:
                print("================")
                cur.close()
                session["id"] = user[0]
                return redirect("/")
            else:
                print('error')
    return render_template("SignIn.html")

@app.route("/signOut")
def logout():
    session["id"] = None
    return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_found.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005,debug=True)