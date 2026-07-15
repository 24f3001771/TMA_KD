#storing all configurations related to app
from flask import Flask

app=None #creating app variable
from application.database import db

def create_app():  #return app object
    app=Flask(__name__)# have to consider this for the code of your server or app...all the methods of flask are applicable to this app also...making app as a flask object
    app.debug=True #detect changes and pin point the error
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///e-dine.sqlite3'
    db.init_app(app)
    app.app_context().push()
    return app

app= create_app() #every configuration made above is applicable to this app object 
from application.controller import * #controller file resides in application folder
if __name__== "__main__": # you have to run this app.py file only when it is invockd directly 
    app.run()


