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
        user=User.query.filter_by(username=username).first()
        if user:
            if user.password==password:
                if user.role=="admin":
                    return redirect('/admin')
                elif user.role=="trek staff":
                    return redirect(f"/home/{user.id}")
                else:
                    return redirect(f"/home/{user.id}")#trekker
            else:
                return render_template("incorrect_p.html")
        else:
            return render_template("not_exist.html")
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        role=request.form.get("role")
        #as i am signing up so i want to check there should be unique email and username
        user_name=User.query.filter_by(username=username).first()
        user_email=User.query.filter_by(email=email).first()
        if user_name or user_email:
            return render_template("already.html")
        else:
            new_user=User(username=username,email=email,password=password,role=role)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
    return render_template("signup.html")

@app.route("/admin")
def admin():
    user=User.query.filter_by(role="admin").first()
    recent_bookings=Booking.query.order_by(Booking.created_at.desc()).limit(4).all()
    treks_count=Trek.query.count()
    user_count=User.query.count()
    staff_count=User.query.filter_by(role="trek staff").count()
    bookings_count=Booking.query.count()
    return render_template("admin_dashboard.html",recent_bookings=recent_bookings,treks_count=treks_count,user_count=user_count,staff_count=staff_count,bookings_count=bookings_count)


@app.route("/treks")
def treks():
    treks=Trek.query.all()
    return render_template("admin_treks.html",treks=treks)

@app.route("/add_treks")
def add_trek():
    return render_template("a_add_treks.html")

@app.route("/home/<int:user_id>")
def home(user_id):
    this_user=User.query.get(user_id)



#Model.query.count()
#Model.query.filter_by(condition).count()