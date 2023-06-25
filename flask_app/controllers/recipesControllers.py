from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.recipes import Recipe
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/add/recipe/page')
def add_page():
    
    return render_template ("add_recipe.html",recipes=Recipe.get_all())

@app.route('/posted/info/<int:id>')
def Posted_info(id):
    
    recipes=Recipe.rcp_user(id)
    users=User.get_one({'id':session['user_id']})
    return render_template ("posted_info.html",users=users,recipes=recipes )


@app.route('/edit/recipe/page/<int:id>')
def edit_page(id):
    
    
    return render_template ("edit_recipe.html", recipes=Recipe.get_one(id))

@app.route('/edit/recipe', methods=['POST'])
def edit_recipe():
    if not Recipe.edit_recipe_msgs(request.form):
        return redirect(f"/edit/recipe/page")
    data = {
        'id': request.form['id'],
        'name': request.form['name'],   
        'desc':request.form['desc'],
        'instr': request.form['instr'],
        'make_time': request.form['make_time'],
        'cook_time': request.form['cook_time'],
    }
    Recipe.update(data)
    return redirect ("/dashboard")

@app.route('/add/recipe', methods=['POST'])
def add_recipe():
    if not Recipe.edit_recipe_msgs(request.form):
        return redirect("/add/recipe/page")
    data = {
        'name': request.form['name'],   
        'desc':request.form['desc'],
        'instr': request.form['instr'],
        'make_time': request.form['make_time'],
        'cook_time': request.form['cook_time'],
        'user_id': request.form['user_id'],
    }
    Recipe.create(data)
    return redirect ("/dashboard")

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    
    Recipe.delete(id)
    return redirect ("/dashboard")

