#business logic
from flask import Flask, render_template, redirect, url_for, request,flash
# #from app import app---> circular import error
from flask import current_app as app

#as i will have all my routes and i will need tables for crud operations so i will require model.py here
from .models import *


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #check if user exists or nor?
        this_user=User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password==password:
                if this_user.role=="admin":
                    return redirect('/admin_dashboard')
                elif this_user.role=="trek staff":
                    return redirect(f"/home/{this_user.id}")
                else:
                    return redirect(f"/home/{this_user.id}")#trekker
            else:
                return render_template("incorrect_p.html")
        else:
            return render_template("not_exist.html")
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        
    return render_template("signup.html")


