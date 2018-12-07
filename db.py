import sqlite3, api

#==========================================================
def init():
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

def setLocation(user, home):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "UPDATE users SET address = '{0}' WHERE username = '{1}'".format(home, user)
    c.execute(command)
    db.commit()
    db.close()

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
    command = "CREATE TABLE IF NOT EXISTS {0} (name TEXT, date TEXT, location TEXT, directions TEXT, url TEXT)".format(user)
    c.execute(command)
    db.commit()
    db.close()

def addEvent(user,name,date,location,direction,url):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()

    command = "INSERT INTO {} VALUES({},{},{},{},{})".format(user,name,date,location,direction,url)
    c.execute(command)

    db.commit()
    db.close()

def displayEvents(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()

    command = "SELECT * FROM {0}".format(user)
    c.execute(command)
    ret = ""
    for i in c.fetchall():
        ret += i + "/n"

    db.commit()
    db.close()
    return ret
