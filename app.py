# #storing all configurations related to app
# from flask import Flask,render_template,request

# app=None #creating app variable
# # from application.database import db

# def create_app():  #return app object
#     app=Flask(__name__)# have to consider this for the code of your server or app...all the methods of flask are applicable to this app also...making app as a flask object
#     app.debug=True #detect changes and pin point the error
#     # app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///e-dine.sqlite3'
#     # db.init_app(app)
#     # app.app_context().push()
#     return app

# app= create_app() #every configuration made above is applicable to this app object 
# # from application.controller import * #controller file resides in application folder



# @app.route("/")
# def login():
#     return render_template("login.html")

# if __name__== "__main__": # you have to run this app.py file only when it is invockd directly 
#     app.run()

from jinja2 import Template
from flask import Flask,redirect,request,render_template,url_for,flash
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3' #database uri setup
db=SQLAlchemy(app)


@app.route("/dashboard")
def open_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email,password)
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        pass
        return redirect("/dashboard")
    return render_template("signup.html")

if __name__=="__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

