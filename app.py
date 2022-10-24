from flask import Flask, render_template, request, url_for, redirect
from flask.wrappers import Request
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, Text
import psycopg2
import config

app = Flask(__name__)
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
    return render_template("HomePageNew.html")

@app.route("/home", methods = ["GET"])
def home_new():
    return render_template("HomePage.html")

@app.route("/rate", methods = ["GET"])
def rate_movie():
    return render_template("RateTheMovie.html")

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
        return render_template("HomePage.html", name = name)
    return render_template("SignUp.html")

@app.route("/signIn", methods = ["GET", "POST"])
def signIn():
    email = request.args.get("email")
    password = request.args.get("password")
    if (email):
        cur = con.cursor()
        cur.execute("select name, email, password from users")
        users = cur.fetchall()
        print(users)
        for user in users:
            if user[1] == email and user[2] == password:
                cur.close()
                return redirect("/")
            else:
                print('error')
    return render_template("SignIn.html")
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_found.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005,debug=True)