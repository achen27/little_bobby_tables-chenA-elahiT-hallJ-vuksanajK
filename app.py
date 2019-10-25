# Team Robert’); DROP TABLE S\*;-- (a.k.a little_bobby_tables)
#       Amanda Chen (PM), Jesse Hall, Kiran Vuksanaj, Tanzim Elahi
# SoftDev1 Pd1
# P00 -- Da Art of Storytellin' (Part X)
# 2019-10-17


from flask import Flask, render_template, request, redirect, url_for,session, flash, get_flashed_messages
import os
import sqlite3
import databasing

#the sqlite part aka db_builder.py
databasing.buildDB()

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

    username=request.form["new_user"]
    print(username)
    password=request.form["new_password"]

    data = databasing.verifyUser(username)
    if(data == 0):
        databasing.addUser(username,password)
        flash('You have successfully created your account, and logged in!')
        session['username']=username
        return redirect(url_for("mystories"))
    else:
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

    result = databasing.verifyUser(username)
    print('huh?')

    if(result == 1): # username and password valid
        session['username'] = username
        flash('You have successfully logged in!')
        return redirect(url_for('mystories'))
    else:
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
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #print(session)
    #print(request.form)
    session.pop('username') #removes session info
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

@app.route("/otherstories")
def otherstories():
    #s = getStories("...")
    if('username' in session):
        username = session['username']
        s = databasing.otherStories(username)
        return render_template('other.html',
                                username=session['username'],
                                stories = s
                                )
    else:
        return redirect(url_for('root'))

@app.route("/modify",methods=['GET'])
def modifypage():
    print(request.method)
    if(not 'username' in session):
        flash('You are not logged in. Please login to access this page.')
        return redirect(url_for('root'))
    username = session['username']
    storyID = request.args['story_id']

    result = databasing.getStory(storyID)

    print(result)

    if(result is None):
        # case: invalid id, no story with such id

        flash('Error occured: no such story with given id')
        return redirect(url_for('mystories'))


    print(result[0])
    return render_template(
        'modify.html',
        storyTitle=result[0],
        lastAuthor=result[3],
        lastEditTime=result[2],
        lastEditContents=result[1],
        story_id=storyID,
        username=username
    )

@app.route("/modify",methods=['POST'])
def contribute_to_story():
    if(not ('username' in session)):
        return redirect(url_for('root'))
    username = session['username']
    story_id = request.form['story_id']
    edit_text = request.form['newedit']

    print(story_id)

    return_alert = databasing.addEdit(username,story_id,edit_text)
    flash(return_alert)
    return redirect(url_for("mystories"))

if __name__ == "__main__":
    app.debug = True
    app.run()
