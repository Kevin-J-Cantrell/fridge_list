from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Item:
    db = 'fridge_list'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount  = data['amount']
        self.msrp  = data['main_price']
        self.salePrice  = data['discounts']
        self.categoryPath  = data['categoryPath']
        self.thumbnailImage  = data['thumbnailImage']
        self.stock  = data['stock']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        many_items = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of users
        output = []
        # Iterate over the db results and create instances of users with cls.
        for item in many_items:
            output.append( cls(item) )
        return output

    @classmethod
    def create(cls, data ):
        query = """
        INSERT INTO items ( f_name , l_name , email , password ) 
        VALUES ( %(f_name)s , %(l_name)s , %(email)s , %(password)s );
                """
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.db).query_db( query, data )
        return result
    
    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM items 
        WHERE id = %(id)s;
                """
        connectToMySQL(cls.db).query_db( query,data )
    
    @classmethod
    def item_user(cls ,itm_id):
        data = {"id": itm_id }
        query = """
        SELECT * FROM items
        JOIN users
        ON items.user_id = users.id
        WHERE items.id = %(id)s
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        user_info = results[0]
        my_recipe = cls (user_info)
        user_data = {
            "id" : user_info["users.id"],
            "f_name" : user_info["f_name"],
            "l_name" : user_info["l_name"],
            "email" : user_info["email"],
            "password" : user_info["password"],
            "created_at" : user_info["users.created_at"],
            "updated_at" : user_info["users.updated_at"]
        }
        my_recipe.user = users.User(user_data)# goes to user.py
        return my_recipe
    
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