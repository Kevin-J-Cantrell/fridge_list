from flask_app import app
from flask_app.controllers import usersControllers
from flask_app.controllers import recipesControllers
from flask_app.controllers import itemsControllers


if __name__ == '__main__':
    app.run(debug=True, port=8000)