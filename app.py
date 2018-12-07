import os

from flask import Flask, render_template, request, session, url_for, redirect, flash, Markup

import db, api


app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def home():
    if 'username' in session: #checks if logged in
        userAddress=db.getLocation(session['username'])
        print(userAddress)
        if 'location' not in session:
            session['location'] = api.toGeo(userAddress)
            #location is set to default if no searches made
        if 'search' not in session:
            session['search'] = userAddress

        location = session['location']

        try:
            events = api.getEvents(location)#check if events are avail
        except:
            session.pop('location')#resets location to default after redirect
            flash('No events at this location, try again.')#error msg
            return redirect('/')

        eventList={} #event IDs are keys, event info is values
        for e in events:#for every
            event = api.getEventInfo(e)
            eventList[api.getId(e)] = event

        if 'id' in session:
            event = eventList[session['id']]
        else:
            event = api.getEventInfo(events[0])

        directions = api.drivingDir(session['location'],event[7])

        if 'artist' in session:
            artist = session['artist']
        else:
            artist = event[4][0]

        albums = api.getAlbums(artist)
        bio = api.getBio(artist)['bio']

        return render_template("home.html", username=session['username'], allEvents=eventList, artists=event[4], eventName=event[0], note =event[11],url=event[9],venue=event[8], address=event[3], searchAddress=session['search'], userAdress=db.getLocation(session['username']), date=event[1],time=event[6],price=event[10],allAlbums=albums, artistBio=bio, artistName=artist, directions=directions['directions'])

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    if len(username) < 3:
        flash('Username must be at least 3 characters, try again.')
        return redirect('/')
    elif len(password) < 3:
        flash('Password must be at least 3 characters, try again.')
        return redirect('/')
    try:
        suggest = api.suggest(address) #list of suggestions based on user input
        if len(suggest) != 0:
            address =  suggest[0]#sets address to first in suggestions
    except:
        flash('Invalid location, try again.')
        return redirect('/')

    if not db.isUser(username):
        db.register(username,password,address)
        flash('Account successfully created!')
    else:
        flash('Username already taken, try again.')
    return redirect('/')


@app.route('/auth', methods=["POST"])
def auth():
    username = request.form['username']
    password = request.form['password']

    session['username'] = username

    if db.isUser(username):
        if db.getPass(username) == password:
            return redirect('/')
        else:
            flash('Wrong password, try again')
            return redirect(url_for('logout'))
    else:
        flash('Username does not exist, try again.')
        return redirect(url_for('logout'))

@app.route('/search', methods=["GET","POST"])
def search():
    search = request.values.get('search')
    try:
        results=[]
        results = api.suggest(search)
        if len(results) != 0:
            search = results[0]
    except:
        flash('Not a valid location, try again.')
        return redirect('/')
    try:
        location = api.toGeo(search)
        session['location'] = location
        session['search'] = search
        if 'artist' in session:
            session.pop('artist')
    except:
        return redirect('/')
    flash('Did you mean ' + search + '? ' )
    return redirect('/')


@app.route('/settings', methods=["GET","POST"])
def settings():
    return render_template("settings.html")

@app.route('/event', methods=["GET","POST"])
def event():
    eventId = list(request.values)[0]
    print("REQ vALUES_______")
    print(list(request.values)[0])
    session['id'] = eventId
    return redirect('/')

@app.route('/artist', methods=["GET","POST"])
def artist():
    artist = list(request.values)[0]
    session['artist'] = artist
    return redirect('/')

@app.route('/updatepass', methods=["GET","POST"])
def updatepass():
    try:
        newPassword = request.form["new_password"]
        confirmPassword = request.form["confirm_new_password"]
        oldPassword = request.form["old_password"]
        user = session['username']
    except:
        flash("Passwords cannot be blank, try again.")
        return redirect("/settings")
    if db.getPass(user) == oldPassword and newPassword == confirmPassword:
        db.setPass(user, newPassword)
        flash("Successfully updated password.")
    else:
        flash("Passwords didn't match, try again.")
        return redirect("/settings")
    return redirect('/logout')

@app.route('/updateaddress', methods=["POST"])
def updateaddress():
    try:
        addr = request.form['new_address']
    except:
        flash('Cannot be blank')
    try:
        results=[]
        results = api.suggest(addr)
        addr = results[0]
        location = api.toGeo(addr)
    except:
        flash('Not a valid location, try again.')
        return redirect('/settings')
    db.setLocation(session['username'],addr)
    msg = 'Successfully updated location.'
    flash(msg)
    return redirect('/logout')


if __name__ == '__main__':
    db.init()
    app.debug = True
    app.run()
