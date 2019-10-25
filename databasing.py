import sqlite3

def buildDB():
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

def verifyUser(user):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command = "SELECT count(*) FROM Accounts WHERE Username=\"{}\";"

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

def addEdit(storyID,edit,time,user):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command="INSERT INTO Accounts VALUES(\"{}\",\"{}\",\"{}\",\"{}\")"
    c.execute( command.format(storyID,edit,time,user) )

    db.commit()
    db.close()

def addStory(storyID,title,story):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command="INSERT INTO Accounts VALUES(\"{}\",\"{}\",\"{}\")"
    c.execute( command.format(storyID,title,story) )

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

def userStories(user):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    command='''
        SELECT
            ID,
            Title,
            Story
        FROM
            Story_List
        INNER JOIN
            Edits using (ID)
        WHERE
            Username=\"{}\";
        '''
    c.execute( command.format(user) )
    results = c.fetchall()

    db.commit()
    db.close()

    return results

def otherStories(user):
    print('get other stories for {}'.format(user))
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    # command = '''
    # i think this could be workable code but the next is more direct
    # SELECT
    #     ID,Title,Username
    # FROM
    #     Story_List
    # LEFT JOIN
    #     Edits USING ( ID )
    # WHERE
    #     Username != '{}';
    # '''
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
                Username=='rubyred' AND ID=Story_List.ID
        );
    '''
    c.execute( command.format(user) )
    results = c.fetchall()
    print(results)

    db.commit()
    db.close()

    return results

def addStory(title,story):
    data="data.db"
    db=sqlite3.connect(data)
    c=db.cursor()

    # determine how many stories already exist
    command = "SELECT count(*) FROM Story_List;"
    newID = c.fetchone()[0]
    print(newID)

    command="INSERT INTO Accounts VALUES(\"{}\",\"{}\",\"{}\")"
    c.execute( command.format(newID,title,story) )

    db.commit()
    db.close()


def addEdit(username,id,editText):
    db = sqlite3.connect('data.db')
    c = db.cursor()
    command = 'select count(*) from Edits where id={} and username="{}"'
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
        print(command)
        print(command.format(id,editText,username))
        c.execute(command.format(username,id,editText))
        db.commit()
        db.close()
        return 'Submission successfully added.'
