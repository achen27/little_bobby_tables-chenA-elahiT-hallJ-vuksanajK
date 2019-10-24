import sqlite3

def buildDB():
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

def verifyUser(user):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command = "SELECT count(*) FROM Accounts WHERE username=\"{}\";"

    countWithUser = c.execute( command.format(user) )
    data = c.fetchone()[0] # i dont get this line? gonna try and figure it out later
    return(data)

    db.commit()
    db.close()

def addUser(user,p):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command="INSERT INTO Accounts VALUES(\"{}\",\"{}\")"
    c.execute( command.format(user,p) )

    db.commit()
    db.close()

def getStory(storyID):
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

    db.commit()
    db.close()

    return result
