from flask import Flask, render_template, request, session, url_for, redirect, flash
import os, db

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def login():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
    

@app.route('/auth', methods=["POST"])
def auth():
    username = request.form['username']
    password = request.form['password']

    session['username'] = username

    if db.isUser(username):
        if db.getPass(username) == password:
            return redirect(url_for('home'))
        else:
            flash('Wrong password')
            return redirect(url_for('logout'))
    else:   
        flash('Username does not exist')
        return redirect(url_for('logout'))
  


@app.route('/home')
def home():
    username = session['username']
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run()
