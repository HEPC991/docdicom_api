import io
from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from routes.selects import select
from routes.deletes import delete
from routes.updates import update
from routes.inserts import insert
from routes.test import test
from routes.validation import validate
from routes.handlers import page_not_found

app = Flask(__name__)

bcrypt = Bcrypt(app)

CORS(app)

conexion = MySQL(app)

app.register_blueprint(select)
app.register_blueprint(delete)
app.register_blueprint(update)
app.register_blueprint(insert)
app.register_blueprint(test)
app.register_blueprint(validate)
app.register_error_handler(404, page_not_found)

