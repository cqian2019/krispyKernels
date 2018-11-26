import sqlite3

#==========================================================

db = sqlite3.connect("krispy.db")
c = db.cursor()
command = "CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT, address TEXT)"
c.execute(command)
command = "CREATE TABLE IF NOT EXISTS events (username TEXT, date TEXT, location TEXT, directions TEXT, url TEXT)"
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


def getPass(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = '{0}'".format(user)
    c.execute(command)
    ret = c.fetchone()[0]
    db.commit()
    db.close()
    return ret

def register(user,pw,home):
    if isUser(user):
        return "user already exists"
    db = sqlite3.connect("krispy.db")
    c = db.cursor()
    command = "INSERT INTO users VALUES(?,?,?)"
    c.execute(command,(user,pw,home,))
    db.commit()
    db.close()
    return "account added"

def addEvent(user,date,location,direction,url):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()

    command = "INSERT INTO events VALUES(?,?,?,?,?)"
    c.execute(command,(user,date,location,direction,url,))

    db.commit()
    db.close()

def displayEvents(user):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()

    command = "SELECT date, location, directions, url FROM events WHERE username = '{0}'".format(user)
    c.execute(command)

    for i in c:
        print(type(i))

    db.commit()
    db.close()

print(register('cheryl','cpass', "homeAddress"))
# print(register('cheryl2','cpass', "homeAddress"))
# print(isUser('cheryl'))
# print(getPass('cheryl'))
# addEvent("cheryl", "today", "location0", "thatWay", "url")
displayEvents("cheryl")

#==========================================================
