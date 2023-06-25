from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash

class Recipe:
    db = 'fridge_list'
    def __init__(self, data):
        self.id = data['id']
        self.rcp_name = data['rcp_name']
        self.desc  = data['desc']
        self.instr  = data['instr']
        self.make_time  = data['make_time']
        self.cook_time  = data['cook_time']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id;"""
        recipe_data = connectToMySQL(cls.db).query_db(query)
        output = []
        for user_info in recipe_data:
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
            output.append( my_recipe)
        return output
    
    @classmethod
    def create(cls, data ):
        query = """
        INSERT INTO recipes ( rcp_name , desc , instr , make_time , cook_time ,user_id ) 
        VALUES ( %(rcp_name)s , %(desc)s , %(instr)s , %(make_time)s , %(cook_time)s , %(user_id)s );"""
        result = connectToMySQL(cls.db).query_db( query, data )
        return result
    
    @classmethod
    def delete(cls,id):
        data = {"id" : id}
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db( query,data )

    @classmethod
    def update(cls,data):
        print("updating")
        query = """
        UPDATE recipes 
        SET rcp_name = %(rcp_name)s , desc = %(desc)s , instr = %(instr)s , make_time = %(make_time)s , cook_time = %(cook_time)s 
        WHERE id = %(id)s;"""
        connectToMySQL(cls.db).query_db( query,data )
        
    @classmethod
    def get_one(cls,id):
        data = {"id": id}
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db( query,data )
        return cls(result[0]) # a list of dictionaries
    
    @classmethod
    def rcp_user(cls ,rcp_id):
        data = {"id": rcp_id }
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s
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
    
    @staticmethod
    def edit_recipe_msgs(recipe):
        is_valid = True
        if len(recipe['rcp_name']) < 5:
            flash("First name must be at least 5 characters")
            is_valid= False
        if len(recipe['desc']) < 2:
            flash("desc field can not be empty")
            is_valid= False
        if len(recipe['instr']) < 2:
            flash("instr field can not be empty")
            is_valid= False
        if len(recipe['make_time']) < 2:
            flash("Date can not be empty")
            is_valid= False
        return is_valid