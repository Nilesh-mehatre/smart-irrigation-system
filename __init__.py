
from datetime import timedelta
from flask import Flask         
from flask_sqlalchemy import SQLAlchemy
import json
with open("config.json","r") as c:
    params=json.load(c)['params']
app=Flask(__name__,template_folder="Templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'

from config import Config
app.config.from_object(Config)

db=SQLAlchemy(app)   



from views import *

with app.app_context():
    db.create_all()
 
if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)