# Team Robert’); DROP TABLE S\*;-- (a.k.a little_bobby_tables)
#       Amanda Chen (PM), Jesse Hall, Kiran Vuksanaj, Tanzim Elahi
# SoftDev1 Pd1
# P00 -- Da Art of Storytellin' (Part X)
# 2019-10-17


from flask import Flask, render_template, request, redirect, url_for,session, flash, get_flashed_messages
import os
import sqlite3
#the sqlite part aka db_builder.py
data="data.db"
db=sqlite3.connect(data)
c=db.cursor()
command="CREATE TABLE if not EXISTS Story_List(ID INTEGER, Title TEXT, Story TEXT)"
c.execute(command)
command="CREATE TABLE if not EXISTS Edits(ID INTEGER,Edit TEXT,Timestamp TIMESTAMP, Username TEXT)"
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
@app.route("/join",methods=['GET']) # the form to sign up
def signuppage():
    return render_template('join.html'); # the method to add account
@app.route("/join",methods=['POST'])
def create():
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    username=request.form["new_user"]
    print(username)
    password=request.form["new_password"]

    command = "SELECT count(*) FROM Accounts WHERE username=\"{}\";"
    countWithUser = c.execute( command.format(username) )
    data = c.fetchone()[0] # i dont get this line? gonna try and figure it out later
    print(data)
    if(data == 0):
        command="INSERT INTO Accounts VALUES(\"{}\",\"{}\")"
        c.execute(command.format(username,password))

        db.commit()
        db.close()
        flash('You have successfully created your account, and logged in!')
        session['username']=username
        return redirect(url_for("mystories"))
    else:
        db.commit()
        db.close()
        flash('Username is taken. Please try again with another username.')
        return redirect(url_for("root"))
    return render_template('homepage.html')


@app.route("/")
def root():
    print(app)
    print(get_flashed_messages())
    if('username' in session):
        flash('You are already logged in!')
        return redirect(url_for("mystories"))
    return render_template('root.html',
                            team = name,
                            rost = roster)

@app.route("/login", methods=['GET']) # the form to login
def loginform():
    return render_template('login.html')

@app.route("/login", methods=['POST']) # the method to login
def authenticate():
    username = request.form['username']
    password = request.form['password']

    db = sqlite3.connect('data.db')
    c = db.cursor()

    command = 'select count(*) from Accounts where username="{}" and password="{}"'
    c.execute(command.format(username,password))
    result = c.fetchone()[0]
    print('huh?')
    if(result == 1): # username and password valid
        session['username'] = username
        db.commit()
        db.close()
        flash('You have successfully logged in!')
        return redirect(url_for('mystories'))
    else:
        db.commit()
        db.close()
        flash('Incorrect username or password.')
        return redirect(url_for('root'))
    return render_template('out.html',
                            team = name,
                            rost = roster,
                            arg_user = str(request.args["username"]),
                            arg_method = str(request.method))

@app.route("/logout")
def logout():
    app.secret_key = os.urandom(32)
    return redirect(url_for('root'))


@app.route("/error")
def err():
    return "blaaa"


@app.route("/mystories")
def mystories():
    if('username' in session):
        return render_template('homepage.html',
                                username=session['username']
                                )
    else:
        return redirect(url_for('root'))

@app.route("/modify",methods=['GET'])
def modifypage():
    print(request.method)
    storyID = request.args['story_id']

    db = sqlite3.connect('data.db')
    c = db.cursor()

    command = '''
    select
        Story_List.Title,
        Edits.Edit,
        Edits.Timestamp,
        Edits.Username
    from
        Story_List
    left join
        Edits using (ID)
    where Story_List.ID={}
    order by Edits.Timestamp desc;
    '''
    c.execute(command.format(storyID,storyID))
    result = c.fetchone()
    print(result)
    if(result is None):
        # case: invalid id, no story with such id
        db.commit()
        db.close()

        flash('Error occured: no such story with given id')
        return redirect(url_for('mystories'))

    db.commit()
    db.close()

    print(result[0])
    return render_template(
        'modify.html',
        storyTitle=result[0],
        lastAuthor=result[3],
        lastEditTime=result[2],
        lastEditContents=result[1]
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
