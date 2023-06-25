from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.items import Item
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/add/item/page')
def add_page():
    
    return render_template ("items.html",items=Item.get_all())

@app.route('/posted/info/<int:id>')
def Posted_info(id):
    
    items=Item.rcp_user(id)
    users=User.get_one({'id':session['user_id']})
    return render_template ("posted_info.html",users=users,items=items )


@app.route('/edit/Item/page/<int:id>')
def edit_page(id):
    
    
    return render_template ("edit_Item.html", items=Item.get_one(id))

@app.route('/edit/Item', methods=['POST'])
def edit_Item():
    if not Item.edit_Item_msgs(request.form):
        return redirect(f"/edit/Item/page")
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

@app.route('/add/Item', methods=['POST'])
def add_Item():
    if not Item.edit_Item_msgs(request.form):
        return redirect("/add/Item/page")
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

@app.route('/delete/Item/<int:id>')
def delete_Item(id):
    
    Item.delete(id)
    return redirect ("/dashboard")

