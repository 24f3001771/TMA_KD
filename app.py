#storing all configurations related to app
from flask import Flask,render_template,request

app=None #creating app variable
from application.database import db #because i have defined db somwhere else

def create_app():  #return app object
    app=Flask(__name__)# have to consider this for the code of your server or app...all the methods of flask are applicable to this app also...making app as a flask object
    app.debug=True #detect changes and pin point the error
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3' #database uri setup
    db.init_app(app) #This connects SQLAlchemy with Flask.
    app.app_context().push()#it should run with the context of database
    return app

app= create_app() #every configuration made above is applicable to this app object 
from application.controller import * #controller file resides in application folder and here we are attaching controller file with app.py



if __name__== "__main__": #if you are running this app from here only then only it will run , not by importing inside any other file
    with app.app_context():
        db.create_all()#create my database when my context of app is created
        #by default create admin
        Admin=User.query.filter_by(role='admin').first()
        if Admin is None:
            Admin=User(username='admin',email='dhullkhushi365@gmail.com',password='16102005',full_name='khushi dhull',phone='123456789',role='admin')
            db.session.add(Admin)
            db.session.commit()
    app.run()