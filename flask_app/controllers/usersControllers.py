import requests
from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    
    return redirect ("/login")

@app.route('/login')
def Login():
    
    return render_template ("login.html")

@app.route('/register/page')
def Register_Page():
    
    return render_template ("register.html")



# @app.route('/dashboard')
# def Dashboard():
#     item_id = "36904791"
#     url = f"https://developer.api.walmart.com/api-proxy/service/affil/product/v2/postbrowse?itemId={item_id}"

#     response = requests.get(url)

#     if response.status_code == 200:
#         # Request was successful
#         json_data = response.json()
#         # Do something with the JSON data
#     else:
#         # Request failed for some reason
#         print(f"Request failed with status code {response.status_code}")

    
    
#     return render_template ("dashboard.html",user=User.get_all())

@app.route('/register', methods=['POST'])
def Register():
    if not User.validate_register(request.form):
        return redirect ("/")
    data = {
        'f_name':request.form['f_name'],
        'l_name' :request.form['l_name'],
        'email'     :request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.create(data)
    return redirect (f"/dashboard")

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect(f"/dashboard")

