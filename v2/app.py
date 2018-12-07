import os

from flask import Flask, render_template, request, session, url_for, redirect, flash, Markup

import db, api


app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def login():
    if 'username' in session:
        if 'location' not in session:
            session['location'] = api.toGeo(db.getLocation(session['username']))

        location = session['location']
        try:
            events = api.getEvents(location[0],location[1])
        except:
            session.pop('location')
            flash('No events at this location, try again')
            return redirect('/')

        eventList={}

        for e in events:
            event=api.getEventInfo(e)
            eventList[api.getId(e)] = event

        if 'lineup' in session:
            lineup = session['lineup']
            eventInfo = session['eventInfo']

        else:
            lineup = api.getLineup(events[0])
            eventInfo = api.getEventInfo(events[0])

            currentGeo = api.toGeo(db.getLocation(session['username']))
            # print(1)
            startStr = str(currentGeo[0]) + ',' + str(currentGeo[1])
            # print(2)
            event = events[0]
            # print(3)
            endStr = api.getEventLocation(event)
            # print(endStr)
            directions = api.drivingDir(startStr, endStr)
            # print(4)
            eventInfo.append(directions['directions'])
            date = api.getDateTime(events[0])
            weather = api.weather(date,endStr)
            weatherInfo = "The weather on that day will be {0} degrees Fahrenheit and has a {1}% chance of precipitation".format(weather['temperature'], weather['Precipitation chance (out of 1):']*100)
            eventInfo.append(weatherInfo)


        lineupStr = ""
        albumStr = ""

        for artist in lineup:
            lineupStr += artist
            lineupStr += "<br>"

        artistName = lineup[0].replace(" ", "+")
        #albumStr = api.getAlbums(artistName)

        return render_template('home.html', username=session['username'], allEvents=eventList, artists=lineup, eventInfo=eventInfo)

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    if 'lineup' in session:
        session.pop('eventInfo')
        session.pop('lineup')

    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    suggest = api.suggest(address)

    if len(suggest) != 0:
        address =  suggest[0]
    else:
        flash('Invalid address, try again')
        return redirect('/')

    if not db.isUser(username):
        db.register(username,password,address)
        flash('Account successfully created! Address auto-completed as ' + address + '. Log in to update.')
    else:
        flash('Username already taken, try again')
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
            flash('Wrong password')
            return redirect(url_for('logout'))
    else:
        flash('Username does not exist')
        return redirect(url_for('logout'))

@app.route('/search', methods=["GET","POST"])
def search():
    search = request.values.get('search')
    print(search)
    results = api.suggest(search)
    if len(results) != 0:
        search = results[0]
    print(search)
    location = []
    try:
        location = api.toGeo(search)
        session['location'] = location
    except:
        flash('Not a valid address, try again')
        return redirect('/')
    return redirect('/')


@app.route('/settings', methods=["GET","POST"])
def settings():
    return render_template("settings.html")

@app.route('/artists', methods=["GET","POST"])
def artists():
    eventId = list(request.values)[0]

    try:
        lineup = api.getLineup(api.getEvent(eventId))
        session['lineup'] = lineup

        eventInfo = api.getEventInfo(api.getEvent(eventId))
        session['eventInfo'] = eventInfo

        print("=======================================================================================================")

        currentGeo = api.toGeo(db.getLocation(session['username']))
        # print(1)
        startStr = str(currentGeo[0]) + ',' + str(currentGeo[1])
        # print(2)
        event = api.getEvent(eventId)
        # print(3)
        endStr = api.getEventLocation(event)
        print(endStr)
        directions = api.drivingDir(startStr, endStr)
        # print(4)
        session['eventInfo'].append(directions['directions'])
        print(session['eventInfo'])
        date = api.getDateTime(event) 
        # print(5)
        weather = api.weather(date,endStr)
        # print(6)
        weatherInfo = "The weather on that day will be {0} degrees Fahrenheit and has a {1}% chance of precipitation".format(weather['temperature'], weather['Precipitation chance (out of 1):']*100)
        # print(7)
        session['eventInfo'].append(weatherInfo)
        # print(8)

    except:
        flash('sorry our api is useless and cant handle too many requests at once.')
        redirect('/')
    return redirect('/')


@app.route('/saveSettings', methods=["GET","POST"])
def saveSettings():
    newPassword = request.form["new_password"]
    confirmPassword = request.form["confirm_new_password"]
    oldPassword = request.form["old_password"]
    user = session['username']
##    address = request.form['address']
    if db.getPass(user) == oldPassword and newPassword == confirmPassword:
##        if '' not in address:
##            db.setLocation(user, address)
        db.setPass(user, newPassword)
        flash("successfully updated password")
    else:
        flash("try again")
    return redirect('/logout')


if __name__ == '__main__':
    app.debug = True
    app.run()
