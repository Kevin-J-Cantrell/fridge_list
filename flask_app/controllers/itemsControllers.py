from flask_app import app
import requests
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.items import Item
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def DashBoard():
    # # Send a request to the Walmart API and retrieve the JSON response
    # url = f"https://developer.api.walmart.com/api-proxy/service/affil/product/v2/postbrowse?itemId={item_id}"
    # response = requests.get(url)
    # data = response.json()

    # # Loop through the items in the JSON response and create new Recipe objects
    # for item in data.get('items', []):
    #     # Extract the relevant information from the JSON data
    #     name = item.get('name')
    #     description = item.get('shortDescription')
    #     image_url = item.get('imageEntities', [{}])[0].get('thumbnailImageUrl')
        
    #     # Create a new Recipe object with the extracted data and save it to the database
    #     items = Item(name=name, description=description, image_url=image_url)
    #     items.save()

    # Retrieve all recipes from the Recipe model
    items = Item.get_all()
    users = User.get_all()
    # Render the template with the list of items
    return render_template("dashboard.html", items=items,users=users)

@app.route('/store/search', methods=["POST","GET"])
def store_search():
    if request.method == 'POST':
        # Retrieve the search query from the form data
        query = request.form['search']

        # Send a request to the Walmart API and retrieve the JSON response
        url = f"https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search?query={query}"
        response = requests.get(url)
        data = response.json()

        # Loop through the items in the JSON response and create new Recipe objects
        for item in data.get('items', []):
            print('item: ', item)
            # Extract the relevant information from the JSON data
            name = item.get('name')
            print('name: ', name)
            description = item.get('shortDescription')
            print('description: ', description)
            image_url = item.get('imageEntities', [{}])[0].get('thumbnailImageUrl')
            print('image_url: ', image_url)

            # Create a new Recipe object with the extracted data and save it to the database
            store_item = Item(name=name, description=description, image_url=image_url)
            print('store_item: ', store_item)
            store_item.save()
            print('store_item: ', store_item)

    # Retrieve all recipes from the Recipe model
    items = Item.get_all()

    # Render the template with the list of recipes and the search form
    return render_template("Dashboard.html", items=items, search_query=query)

@app.route('/edit/item/page/<int:id>')
def edit_item_page(id):
    
    
    return render_template ("edit_item.html", items=Item.get_one(id))

@app.route('/edit/Item', methods=['POST'])
def edit_item():
    if not Item.edit_Item_msgs(request.form):
        return redirect(f"/edit/item/page")
    data = {
        'id': request.form['id'],
        'name': request.form['name'],   
        'desc':request.form['desc'],
        'instr': request.form['instr'],
        'make_time': request.form['make_time'],
        'cook_time': request.form['cook_time'],
    }
    Item.update(data)
    return redirect ("/dashboard")


@app.route('/add/item', methods=['POST'])
def add_item():
    if not Item.edit_Item_msgs(request.form):
        return redirect("/item/page")
    data = {
        'name': request.form['name'],   
        'desc':request.form['desc'],
        'instr': request.form['instr'],
        'make_time': request.form['make_time'],
        'cook_time': request.form['cook_time'],
        'user_id': request.form['user_id'],
    }
    Item.create(data)
    return redirect ("/dashboard")

@app.route('/delete/item/<int:id>')
def delete_item(id):
    
    Item.delete(id)
    return redirect ("/dashboard")

