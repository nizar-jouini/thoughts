from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def log_and_reg():
    if 'user_id' in session:
        return redirect('/thoughts')

    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # If form data are incorrect, just redirect back to root.
    if not User.validation_registration(request.form):
        return redirect("/")
    
    # If form data are correct, save user to database and redirect to root.
    User.register(request.form)
    return redirect("/thoughts")

@app.route('/login', methods=['POST'])
def login():
    if not User.validation_login(request.form):
        return redirect("/")
    
    return redirect("/thoughts")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
