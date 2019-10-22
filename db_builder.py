import sqlite3
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
