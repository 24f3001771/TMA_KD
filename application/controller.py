#business logic
from flask import Flask, render_template, redirect, url_for, request,flash
# #from app import app---> circular import error
from flask import current_app as app
from datetime import datetime
#as i will have all my routes and i will need tables for crud operations so i will require model.py here
from .models import *


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #check if user exists or nor?
        user=User.query.filter_by(username=username).first()
        if not user:
            return render_template("not_exist.html")
        if user.password != password:
            return render_template("incorrect_p.html")
        staff=user.staff_profile
        if user:
            if user.password==password:
                if user.role=="admin":
                    return redirect('/admin')
                elif user.role=="trek staff":
                    if staff.approval_status == "pending":
                        return redirect(f"/staff/{staff.id}/profile")

                    elif staff.approval_status == "approved":
                        return redirect(f"/staff/{staff.id}/dashboard")
                    
                    else:
                        return render_template("staff_rejected.html",status=staff.approval_status)
                else:
                    return redirect(f"/home/{user.id}/dashboard")
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
            if role == "trek staff":
                staff=Staff_profile(user_id=new_user.id,approval_status="pending")
                db.session.add(staff)
            db.session.commit()
            return redirect("/login")
    return render_template("signup.html")

#-----------------------------------handling admin dashboard-----------------------------------------------------------#

@app.route("/admin")
def admin():
    user=User.query.filter_by(role="admin").first()
    recent_bookings=Booking.query.order_by(Booking.created_at.desc()).limit(4).all()
    treks_count=Trek.query.count()
    user_count=User.query.count()
    staff_count=User.query.filter_by(role="trek staff").count()
    bookings_count=Booking.query.count()
    return render_template("admin_dashboard.html",user=user,recent_bookings=recent_bookings,treks_count=treks_count,user_count=user_count,staff_count=staff_count,bookings_count=bookings_count)

@app.route("/admin/bookings")
def bookings():
    bookings=Booking.query.all()
    user=User.query.filter_by(role="admin").first()
    return render_template("a_bookings.html",bookings=bookings,user=user)

@app.route("/admin/treks")
def manage_treks():
    treks=Trek.query.all()
    user=User.query.filter_by(role="admin").first()
    return render_template("admin_treks.html",treks=treks,user=user)

@app.route("/delete/<int:trek_id>/trek")
def delete(trek_id):
    trek=Trek.query.get(trek_id)
    if not trek:
        return render_template("not_found_t.html")
    db.session.delete(trek)
    db.session.commit()

    return redirect("/admin/treks")


@app.route("/admin/add_treks", methods=["GET", "POST"])
def add_trek():

    user=User.query.filter_by(role="admin").first()
    staffs=Staff_profile.query.filter_by(approval_status='approved').all()

    if request.method=="POST":
        name=request.form.get("tname")
        location=request.form.get("loc")
        difficulty=request.form.get("values")
        duration_days=request.form.get("duration")
        max_slots=request.form.get("max slots")
        start_date=datetime.strptime(request.form.get("starttime"),"%Y-%m-%d")
        end_date=datetime.strptime(request.form.get("endtime"),"%Y-%m-%d")
        staff_ids=request.form.getlist("staff_ids")
        status=request.form.get("status")
        description=request.form.get("message")
        staffs_assigned=Staff_profile.query.filter(Staff_profile.id.in_(staff_ids)).all()
        trek=Trek(name=name,location=location,difficulty=difficulty,duration_days=duration_days,start_date=start_date,end_date=end_date,status=status,description=description,max_slots=max_slots)
        db.session.add(trek)
        trek.assigned_staffs.extend(staffs_assigned)
        db.session.commit()
        # flash("Trek added successfully.")
        return redirect(url_for("manage_treks"))
    
    return render_template("a_add_treks.html",trek=None,user=user,staffs=staffs)

@app.route("/update/<int:trek_id>/trek",methods=['POST','GET'])
def update_trek(trek_id):
    trek=Trek.query.get(trek_id)
    user=User.query.filter_by(role='admin').first()
    staffs=Staff_profile.query.filter_by(approval_status='approved').all()
    if not trek:
        return render_template("not_found_t.html")
    if request.method=='POST':
        trek.name=request.form.get("tname")
        trek.location = request.form.get("loc")
        trek.difficulty = request.form.get("values")
        trek.duration_days = request.form.get("duration")
        trek.max_slots = request.form.get("max slots")
        trek.start_date = datetime.strptime(
            request.form.get("starttime"),
            "%Y-%m-%d"
        )

        trek.end_date = datetime.strptime(
            request.form.get("endtime"),
            "%Y-%m-%d"
        )

        trek.status = request.form.get("status")
        trek.description = request.form.get("message")
        staff_ids = request.form.getlist("staff_ids")
        staffs_assigned=Staff_profile.query.filter(Staff_profile.id.in_(staff_ids)).all()

         #replace old staff assignments
        trek.assigned_staffs=staffs_assigned
        db.session.commit()
        return redirect(url_for("manage_treks"))

    return render_template("a_add_treks.html",trek=trek,staffs=staffs,user=user)

@app.route("/admin/staff")
def staff():
    user=User.query.filter_by(role="admin").first()
    status=request.args.get("status","pending") # by default pending
    staffs=Staff_profile.query.filter_by(approval_status=status).all()
    staff_pending = Staff_profile.query.filter_by(approval_status="pending").count()
    staff_approved = Staff_profile.query.filter_by(approval_status="approved").count()
    staff_blacklisted = Staff_profile.query.filter_by(approval_status="blacklisted").count()
    return render_template("a_staff.html",staffs=staffs,staff_pending=staff_pending,staff_approved=staff_approved,staff_blacklisted=staff_blacklisted,user=user,status=status)

@app.route("/approve/<int:staff_id>")
def approve(staff_id):
    staff=Staff_profile.query.get(staff_id)
    if not staff:
        return render_template("s_not_exists.html")
    staff.approval_status="approved"
    db.session.commit()
    return redirect("/admin/staff")

@app.route("/reject/<int:staff_id>")
def reject(staff_id):
    staff=Staff_profile.query.get(staff_id)
    if not staff:
        return render_template("s_not_exists.html")
    staff.approval_status = "blacklisted"
    db.session.commit()
    return redirect("/admin/staff")


@app.route("/admin/users")
def users():
    pass

# --------------------handling staff routes----------------------#
@app.route("/staff/<int:staff_id>/profile",methods=['POST','GET'])
def profile(staff_id):
    staff=Staff_profile.query.get(staff_id)
    if not staff:
        return render_template("s_not_exists.html")
    if staff and staff.profile_completed:
        return render_template("staff_pending.html")

    if request.method=="POST":
        staff.contact_details = request.form.get("contact")
        staff.bio = request.form.get("bio")
        staff.expertise = request.form.get("expertise")
        staff.certifications = request.form.get("certifications")
        staff.years_experience = request.form.get("experience")
        staff.profile_completed = True
        db.session.commit()
        # flash("Profile updated successfully!")
        return render_template("staff_pending.html")
    return render_template("staff_pending_form.html",staff=staff)


@app.route("/staff/<int:staff_id>/dashboard")
def staff_home(staff_id):
    pass



@app.route("/home/dashboard")
def home():
    pass

@app.route("/book/<int:trek_id>")
def book_trek(trek_id):
    pass

# trek.available_slots -= booking.num_participants
# trek.available_slots += booking.num_participants


#Model.query.count()
#Model.query.filter_by(condition).count()

# status = request.args.get("status", "pending")

# staffs = Staff.query.filter_by(status=status).all()

# return render_template(
#     "manage_staff.html",
#     staffs=staffs,
#     status=status
# )
# from flask import session
# session["user_id"] = user.id
# user = User.query.get(session["user_id"])
# What happens when the user logs out?
# session.clear()
# session.pop("user_id")



'''
@app.route("/staff/<int:staff_id>/profile", methods=["GET", "POST"])
def staff_profile(staff_id):

    staff = Staff_profile.query.get_or_404(staff_id)

    if request.method == "POST":

        staff.contact_details = request.form.get("contact")
        staff.bio = request.form.get("bio")
        staff.expertise = request.form.get("expertise")
        staff.certifications = request.form.get("certifications")
        staff.years_experience = request.form.get("experience")

        db.session.commit()

        flash("Profile updated successfully!")

        return redirect(f"/staff/{staff.id}/profile")

    return render_template(
        "staff_profile.html",
        staff=staff
    )


@app.route("/staff/<int:staff_id>/dashboard")
def staff_dashboard(staff_id):

    staff = Staff_profile.query.get_or_404(staff_id)

    return render_template(
        "staff_dashboard.html",
        staff=staff
    )
    '''
