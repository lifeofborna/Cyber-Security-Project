from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

app = Flask(__name__)

#Flaw 5
#csrf = CSRFProtect(app)
#from forms import RegistrationForm

#@app.route('/register', methods=['GET', 'POST'])
#@csrf.exempt  # Exempting CSRF protection for this route
#def register():
#    if 'username' in session:
#        return redirect(url_for('main'))

#    form = RegistrationForm()

#    if form.validate_on_submit():
#        username = form.username.data
#        password = form.password.data

        # Process registration logic

#        session['username'] = username
#        return redirect(url_for('login'))

#    return render_template('register.html', form=form)


#Flaw #3
app.config['SECRET_KEY'] = 'is_this_really_secure_?'
#Fix for the flaw
# import os
# app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY', 'default_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))


@app.route('/')
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    else:
        return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        #Flaw #2
        query = text(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")  # SQL Injection vulnerability

        #We can fix it by replacing the code with :
        # query = text("SELECT * FROM user WHERE username = :username AND password = :password")
        # query = query.bindparams(username=username, password=password)

    
        user = db.session.execute(query).first()

        if user:
            session['username'] = user.username
            return redirect(url_for('main'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('main'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
    # Flaw #1 
    # Fix : 
    #    password = generate_password_hash(password)
    
    
        query = text(f"INSERT INTO user (username, password) VALUES ('{username}', '{password}')")

        
        db.session.execute(query)
        db.session.commit()

        session['username'] = username
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/logout')
def logout():

    #Flaw 4
    session.pop('username', None)
    return redirect(url_for('login'))
    
    #Fixed code:

#    if 'username' in session:
#        session.pop('username', None)
#    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
