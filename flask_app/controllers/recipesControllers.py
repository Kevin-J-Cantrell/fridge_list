import requests
from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.recipes import Recipe
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# @app.route('/recipe/page')
# def recipe_page():

#     item_id = "36904791"
#     url = f"https://developer.api.walmart.com/api-proxy/service/affil/product/v2/postbrowse?itemId={item_id}"
#     response = requests.get(url)
    
#     # Do something with the response, like print the JSON data
#     print(response.json())
#     return render_template ("recipes.html",recipes=Recipe.get_all())

# ----------------------------------------------------------------------

@app.route('/recipe/page/<item_id>')
def recipe_page(item_id):
    # Send a request to the Walmart API and retrieve the JSON response
    url = f"https://developer.api.walmart.com/api-proxy/service/affil/product/v2/postbrowse?itemId={item_id}"
    response = requests.get(url)
    data = response.json()

    # Loop through the items in the JSON response and create new Recipe objects
    for item in data.get('items', []):
        # Extract the relevant information from the JSON data
        name = item.get('name')
        description = item.get('shortDescription')
        image_url = item.get('imageEntities', [{}])[0].get('thumbnailImageUrl')
        
        # Create a new Recipe object with the extracted data and save it to the database
        recipe = Recipe(name=name, description=description, image_url=image_url)
        recipe.save()

    # Retrieve all recipes from the Recipe model
    recipes = Recipe.get_all()
    
    # Render the template with the list of recipes
    return render_template("recipes.html", recipes=recipes)

# ----------------------------------------------------------------------------------

@app.route('/edit/recipe/page/<int:id>')
def edit_recipe_page(id):
    
    
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

