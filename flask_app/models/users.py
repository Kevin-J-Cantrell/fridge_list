from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = 'fridge_list'
    def __init__(self, data):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name  = data['l_name']
        self.email      = data['email']
        self.password   = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        things = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of users
        output = []
        # Iterate over the db results and create instances of users with cls.
        for stuff in things:
            output.append( cls(stuff) )
        return output

    @classmethod
    def create(cls, data ):
        query = """
        INSERT INTO users ( f_name , l_name , email , password ) 
        VALUES ( %(f_name)s , %(l_name)s , %(email)s , %(password)s );
                """
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.db).query_db( query, data )
        return result
    
    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM users 
        WHERE id = %(id)s;
                """
        connectToMySQL(cls.db).query_db( query,data )

    
    @classmethod
    def update(cls,data):
        print("updating")
        query = """
        UPDATE users 
        SET f_name = %(f_name)s , l_name = %(l_name)s , email = %(email)s 
        WHERE id = %(id)s;
                """
        connectToMySQL(cls.db).query_db( query,data )
    @classmethod
    def show(cls,data):
        query = """
        SELECT * FROM users 
        WHERE id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db( query,data ) # a list
        return cls(result[0])
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['f_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['l_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])