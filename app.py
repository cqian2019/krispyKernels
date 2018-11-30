from flask import Flask, render_template, request, session, url_for, redirect, flash, Markup
import os, db, api

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def login():
    if 'username' in session:
        location = api.toGeo(db.getLocation(session['username']))
        events = api.getEvents(location[0],location[1])
        s = ""
        for e in events:
            s += '<input type="radio" name="event" value="' + api.getId(e) + '">'
            s += api.getName(e) + "<br>"
            s += api.getDate(e)  + "<br>"
            s += api.getVenue(e) + "<br>"
            s += api.getGenre(e) + "<br>"
            s += api.getUrl(e) + "<br>"
            s += api.getAddress(e) + "<br><br>"
        return render_template('home.html', username=session['username'], info = Markup(s))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    if not db.isUser(username):
        db.register(username,password,address)
        flash('Account successfully created')
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
        search = results[0][0]
    print(search)
    location = api.toGeo(search)
    print(location)
    events = api.getEvents(location[0],location[1])
    s = ""
    for e in events:
        s += '<input type="radio" name="event" value="' + api.getId(e) + '">'
        s += api.getName(e) + "<br>"
        s += api.getDate(e)  + "<br>"
        s += api.getVenue(e) + "<br>"
        s += api.getGenre(e) + "<br>"
        s += api.getUrl(e) + "<br>"
        s += api.getAddress(e) + "<br><br>"
    return render_template('home.html', info = Markup(s))
@app.route('/settings', methods=["GET","POST"])
def settings():
    return render_template("settings.html")

@app.route('/saveSettings', methods=["GET","POST"])
def saveSettings():
    newPassword = request.form["new_password"]
    confirmPassword = request.form["confirm_new_password"]
    oldPassword = request.form["old_password"]
    user = session['username']
    if db.getPass(user) == oldPassword and newPassword == confirmPassword:
        db.setPass(user, newPassword)
        flash("successfully updated password")
    else:
        flash("try again")
    return redirect('/logout')


if __name__ == '__main__':
    app.debug = True
    app.run()
