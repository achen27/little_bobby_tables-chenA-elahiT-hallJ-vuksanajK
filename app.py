# Team Robert’); DROP TABLE S\*;-- (a.k.a little_bobby_tables)
#       Amanda Chen (PM), Jesse Hall, Kiran Vuksanaj, Tanzim Elahi
# SoftDev1 Pd1
# P00 -- Da Art of Storytellin' (Part X)
# 2019-10-17


from flask import Flask, render_template, request, redirect, url_for,session
import os
import sqlite3
#the sqlite part aka db_builder.py
data="data.db"
db=sqlite3.connect(data)
c=db.cursor()
command="CREATE TABLE if not EXISTS Story_List(ID INTEGER,Story TEXT)"
c.execute(command)
command="CREATE TABLE if not EXISTS Edits(ID INTEGER,Edit TEXT,Username TEXT)"
c.execute(command)
command="CREATE TABLE if not EXISTS Accounts(Username TEXT,Password TEXT)"
c.execute(command)
db.commit()
db.close()
#the flask part
app = Flask(__name__)
name = "Storybuilder"
roster = "little_bobby_tables"
app.secret_key=os.urandom(32)
@app.route("/join")
def create():
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()
    username=request.args["new_user"]
    print(username)
    password=request.args["new_password"]
    command="INSERT INTO Accounts VALUES(\"{}\",\"{}\")"
    c.execute(command.format(username,password))
    db.commit()
    db.close()
    session['username']=username
    return render_template('homepage.html')


@app.route("/")
def root():
    print(app)
    return render_template('root.html',
                            team = name,
                            rost = roster)
@app.route("/auth")
def authenticate():
    return render_template('out.html',
                            team = name,
                            rost = roster,
                            arg_user = str(request.args["username"]),
                            arg_method = str(request.method))


@app.route("/error")
def err():
    return "blaaa"

if __name__ == "__main__":
    app.debug = True
    app.run()
