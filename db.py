import sqlite3, api

#==========================================================

db = sqlite3.connect("krispy.db")
c = db.cursor()
command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, address TEXT)"
c.execute(command)
db.commit()
db.close()

#==========================================================

def isUser(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "SELECT username FROM users WHERE username = '{0}'".format(user)
    c.execute(command)
    ret = False
    if c.fetchone() != None:
        ret = True
    db.commit()
    db.close()
    return ret

def getLocation(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "SELECT address FROM users WHERE username = '{0}'".format(user)
    c.execute(command)
    ret = c.fetchone()[0]
    db.commit()
    db.close()
    return ret

def getPass(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = '{0}'".format(user)
    c.execute(command)
    ret = c.fetchone()[0]
    db.commit()
    db.close()
    return ret

def setPass(user, pw):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "UPDATE users SET password = '{0}' WHERE username = '{1}'".format(pw, user)
    c.execute(command)
    db.commit()
    db.close()

def register(user,pw,home):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    
    command = "INSERT INTO users VALUES(?,?,?)"
    c.execute(command,(user,pw,home,))
    command = "CREATE TABLE IF NOT EXISTS {0} (date TEXT, name TEXT, location TEXT, directions TEXT, url TEXT)".format(user)
    c.execute(command)
    db.commit()
    db.close()

def addEvent(user,date,location,direction,url):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()

    command = "INSERT INTO ? VALUES(?,?,?,?,?)"
    c.execute(command,(user,name,date,location,direction,url,))

    db.commit()
    db.close()

def displayEvents(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()

    command = "SELECT * FROM {0} WHERE username = '{1}'".format(user)
    c.execute(command)

    for i in c.fetchall():
        print(type(i))

    db.commit()
    db.close()



register('u','p','345 Chambers Street')


#==========================================================
