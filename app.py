import os

from flask import Flask, render_template, request, session, url_for, redirect, flash, Markup

import db, api


app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def login():
    if 'username' in session: #checks if logged in
        if 'location' not in session: #checks if user searched
            session['location'] = api.toGeo(db.getLocation(session['username']))
            #location is set to default if no searches made
        location = session['location']#set to search location if search was made

        try:
            events = api.getEvents(location[0],location[1])#check if events are avail
        except:
            session.pop('location')#resets location to default after redirect
            flash('No events at this location, try again.')#error msg
            return redirect('/')

        eventList={} #event IDs are keys, event info is values
        for e in events:#for every
            event=[]
            event.append(api.getName(e))
            event.append(api.getDate(e))
            event.append(api.getVenue(e))
            event.append(api.getGenre(e))
            event.append(api.getAddress(e))
            eventList[api.getId(e)] = event

        if 'lineup' in session: #checks if user selected an event
            lineup = session['lineup']
        else:
            lineup = api.getLineup(events[0])#sets lineup to lineup of 1st event if none selecte

        if 'artist' in session:#checks if user selected an artist
            artist = session['artist'].replace(" ", "+")
        else:
            artist = lineup[0].replace(" ", "+")#sets artist to first on lineup if none selected


        albums = api.getAlbums(artist)
        info = api.getInfo(artist)

        return render_template('home.html', username=session['username'], allEvents=eventList, artists=lineup, allAlbums=albums, artistInfo=info)

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    suggest = api.suggest(address) #list of suggestions based on user input

    if len(suggest) != 0:
        address =  suggest[0][0]#sets address to first in suggestions
    else:
        flash('Invalid address, try again')
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
    results = api.suggest(search)
    if len(results) != 0:
        search = results[0][0]
    location = []
    try:
        location = api.toGeo(search)
        session['location'] = location
        session.pop('lineup')
    except:
        flash('Not a valid address, try again.')
        return redirect('/')
    flash('Location auto-completed to ' + search + '. ' )
    return redirect('/')


@app.route('/settings', methods=["GET","POST"])
def settings():
    return render_template("settings.html")

@app.route('/event', methods=["GET","POST"])
def event():
    eventId = list(request.values)[0]
    try:
        lineup = api.getLineup(api.getEvent(eventId))
        session['lineup'] = lineup
        session['artist'] = lineup[0]
    except:
        flash('Sorry, our api is useless and cant handle too many requests at once.')
        redirect('/')
    return redirect('/')

@app.route('/artist', methods=["GET","POST"])
def artist():
    artist = list(request.values)[0]
    session['artist'] = artist
    return redirect('/')

@app.route('/saveSettings', methods=["GET","POST"])
def saveSettings():
    newPassword = request.form["new_password"]
    confirmPassword = request.form["confirm_new_password"]
    oldPassword = request.form["old_password"]
    user = session['username']
    if db.getPass(user) == oldPassword and newPassword == confirmPassword:
        db.setPass(user, newPassword)
        flash("Successfully updated password.")
    else:
        flash("Try again.")
    return redirect('/logout')


if __name__ == '__main__':
    app.debug = True
    db.init()
    app.run()
