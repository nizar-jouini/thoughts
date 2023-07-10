from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask_app import app
from flask import session , flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

class User:

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod 
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        results = connectToMySQL(DB).query_db(query, data)
        
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def register(cls, data):
        encrypted_password = bcrypt.generate_password_hash(data['password'])

        new_dict = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': encrypted_password
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(DB).query_db(query, new_dict)
        session['user_id'] = results
        return results
    
    @staticmethod
    def validation_registration(user):
        is_valid = True
        user_in_db = User.get_by_email(user)
        if user_in_db:
            flash("Email already exists!","register")
            is_valid = False
        if not User.EMAIL_REGEX.match(user['email']):
            flash("Invalid email!","register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters!","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters!","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!","register")
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash("Passwords don't match!","register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validation_login(user):
        is_valid = True
        user_in_db = User.get_by_email({'email' : user['email']})
        if not user_in_db:
            flash("Email is not associated with an account!","login")
            is_valid = False
        if not User.EMAIL_REGEX.match(user['email']):
            flash("Invalid email!","login")
            is_valid = False
        if user_in_db:
            if not bcrypt.check_password_hash(user_in_db.password, user['password']):
                flash("Incorrect Password!","login")
                is_valid = False
        if is_valid == True:
            session['user_id'] = user_in_db.id
        return is_valid

