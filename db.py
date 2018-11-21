import sqlite3   

#==========================================================

db = sqlite3.connect("krispy.db")
c = db.cursor()  
command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"     
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
    
def register(user,pw):
    db = sqlite3.connect("krispy.db")
    c = db.cursor()  
    command = "INSERT INTO users VALUES(?,?)"
    c.execute(command,(user,pw,))
    db.commit()
    db.close()

#register('cheryl','cpass')
#print(isUser('cheryl'))
#print(getPass('cheryl'))


#==========================================================


