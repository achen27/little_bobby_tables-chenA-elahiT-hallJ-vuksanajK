import sqlite3, hashlib

def buildDB(): #builds a database with three tables
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()
    command="CREATE TABLE if not EXISTS Story_List(ID INTEGER PRIMARY KEY, Title TEXT, Story TEXT)"
    c.execute(command)
    command="CREATE TABLE if not EXISTS Edits(ID INTEGER,Edit TEXT,Timestamp TIMESTAMP, Username TEXT)"
    c.execute(command)
    command="CREATE TABLE if not EXISTS Accounts(Username TEXT,Password TEXT)"
    c.execute(command)
    db.commit()
    db.close()

def verifyUser(user): #searches database if user exists
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command = "SELECT count(*) FROM Accounts WHERE Username=\"{}\";"

    countWithUser = c.execute( command.format(user) )
    data = c.fetchone()[0]
    return(data)

    db.commit()
    db.close()

def rightLogin(user,givenPass): #searches database to match username and password
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()
    command='''
             Select Password
             From Accounts
             Where Username=\"{}\"
         '''
    c.execute(command.format(user))
    info=c.fetchone()

    if not info is None and (hashlib.md5((givenPass.encode('utf-8')))).hexdigest()==info[0]:
        return 1 #correct
    else:
        return 2 #incorrect
    db.commit()
    db.close()

def addUser(user,p): #adds user name and pass into database
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command="INSERT INTO Accounts VALUES(\"{}\",\"{}\")"

    c.execute( command.format(user,(hashlib.md5(p.encode('utf-8'))).hexdigest()) )

    db.commit()
    db.close()

def getStory(storyID): #returns row requested
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

def userStories(user): #list of stories user has contributed to
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command='''
        SELECT
            ID,Title
        FROM
            Story_List
        WHERE
            EXISTS (
                SELECT Username
                FROM Edits
                WHERE
                    Username==\'{}\' AND ID=Story_List.ID
            );
        '''
    c.execute( command.format(user) )
    results = c.fetchall()
    print(results)

    db.commit()
    db.close()

    return results

def otherStories(user): #list of stories user has not contributed to
    print('get other stories for {}'.format(user))
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command = '''
    SELECT
        ID,Title
    FROM
        Story_List
    WHERE
        NOT EXISTS (
            SELECT Username
            FROM Edits
            WHERE
                Username==\'{}\' AND ID=Story_List.ID
        );
    '''
    c.execute( command.format(user) )
    results = c.fetchall()
    db.commit()
    db.close()
    return results


def addEdit(username,id,editText): #adds contribution to database
    db = sqlite3.connect('data.db')
    c = db.cursor()
    command = 'select count(*) from Edits where id=\"{}\" and username=\"{}\"'
    c.execute(command.format(id,username))
    if(c.fetchone()[0] > 0):
        db.commit()
        db.close()
        return 'You have already contributed to this story!'
    else:
        command = '''
        insert into Edits
            (ID,Edit,Timestamp,Username)
        values
            ('{}','{}',datetime('now'),'{}');
        '''

        c.execute(command.format(id,editText,username))
        db.commit()
        db.close()
        return 'Submission successfully added.'

def story(id): #gets the content of the stories
    db = sqlite3.connect('data.db')
    c = db.cursor()
    command='''Select Story, Title
             From Story_List
             Where ID={}
             '''
    c.execute(command.format(id))
    result=c.fetchone()
    db.commit()
    db.close()
    return result

def update(text,story_id): #updates full story
    db=sqlite3.connect('data.db')
    c=db.cursor()
    command='''
            Select Story
            From Story_List
            Where ID=\"{}\"
            '''
    c.execute(command.format(story_id))
    info=c.fetchone()[0]
    info=info+" "+text
    command='''
            UPDATE Story_List
            SET Story=\"{}\"
            WHERE ID=\"{}\"
            '''
    c.execute(command.format(info,story_id))
    db.commit()
    db.close()

def addStory(title,story): #adds a new story to database
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    # determine how many stories already exist
    command = "SELECT count(*) FROM Story_List;"
    c.execute(command)
    newID = c.fetchone()[0]
    print(newID)

    command="INSERT INTO Story_List VALUES(\"{}\",\"{}\",\"{}\")"
    c.execute( command.format(newID,title,story) )

    db.commit()
    db.close()

    return newID

def userHasEdited(username,id): # checks whether story should be visible to user
    db = sqlite3.connect('data.db')
    c = db.cursor()

    command="select count(*) from Edits where ID={} and Username=\'{}\'"
    c.execute(command.format(id,username))
    countEdits = c.fetchone()[0]

    db.commit()
    db.close()

    return countEdits == 1
