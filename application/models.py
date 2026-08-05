from .database import db  #.database means current folder
from sqlalchemy import Enum

#assosiation or junction table (relationship table between staff and trek (many-to-many))
trek_staff_assignment = db.Table("trek_staff_assignment",
    db.Column('trek_id', db.Integer , db.ForeignKey('trek.id'),primary_key=True),
    db.Column('staff_id', db.Integer , db.ForeignKey('staff_profile.id'),primary_key=True),
    db.Column('assigned_at',db.DateTime, default=db.func.now()),
    db.Column('role_on_trek',db.String(),nullable=True)
    )


class User(db.Model):
    __tablename__='user'
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    email=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    full_name        = db.Column(db.String(), nullable=True)
    phone            = db.Column(db.String(), nullable=True)
    role=db.Column(Enum('admin','trek staff','trekker',name='user_role'),nullable=False,default='trekker')# admin | trek staff | trekker
    is_blacklisted=db.Column(db.Boolean,default=False)
    blacklist_reason=db.Column(db.Text,nullable=True)
    is_active=db.Column(db.Boolean,default=True)
    created_at       = db.Column(db.DateTime, default=db.func.now())
    updated_at       = db.Column(db.DateTime, onupdate=db.func.now())

    #Relationships
    #with booking table one user can have multiple bookings but only one booking will belong to only one user
    bookings=db.relationship('Booking',lazy=True, back_populates='user')
    staff_profile=db.relationship('Staff_profile',lazy=True,uselist=False,back_populates='user') #uselist= False means One-to-one (single object) while default it is one-to-many

    # parent table - define relationship
    # child table- define foreign key

    # lazy=true means if i fetch user data till i don't fetch staf-profiles it shouldnt be loaded

class Staff_profile(db.Model):
    __tablename__='staff_profile'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),unique=True,nullable=False)#one to one relationship no multiple ids
    contact_details=db.Column(db.String(),nullable=True)
    bio=db.Column(db.Text,nullable=True)
    expertise=db.Column(db.String(),nullable=True)
    certifications   = db.Column(db.Text, nullable=True)
    years_experience = db.Column(db.Integer, nullable=True)
    approval_status  = db.Column(Enum('pending','approved','blacklisted',name='approval_status'), nullable=False, default='pending')  # pending | approved | blacklisted
    is_available     = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime,default=db.func.now())
    updated_at = db.Column(db.DateTime,default=db.func.now())
    profile_completed = db.Column(db.Boolean,default=False)

    #Relationships
    assigned_treks=db.relationship('Trek',secondary='trek_staff_assignment',lazy=True,back_populates='assigned_staffs')
    user=db.relationship('User',back_populates='staff_profile',lazy=True)


class Trek(db.Model):
    __tablename__='trek'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(), nullable=False)
    description     = db.Column(db.Text, nullable=True)
    location        = db.Column(db.String(), nullable=True)
    difficulty      = db.Column(db.String(), nullable=False, default='moderate')  # easy | moderate | hard
    duration_days   = db.Column(db.Integer, nullable=False)
    start_date      = db.Column(db.DateTime, nullable=True)
    end_date        = db.Column(db.DateTime, nullable=True)
    max_slots       = db.Column(db.Integer, nullable=False, default=20)
    available_slots = db.Column(db.Integer, nullable=False, default=20)
    price           = db.Column(db.Numeric, nullable=False, default=0.0)
    status          = db.Column(Enum('pending','approved','open','closed','completed','cancelled',name='trek_status'),nullable=False, default='pending')  # pending | approved | open | closed | completed | cancelled
    created_at      = db.Column(db.DateTime, default=db.func.now())
    updated_at      = db.Column(db.DateTime, onupdate=db.func.now())
    

    #Relationships
    assigned_staffs=db.relationship('Staff_profile',secondary='trek_staff_assignment',lazy=True,back_populates='assigned_treks')#many to many relationship

    bookings=db.relationship('Booking',back_populates='trek',lazy=True)#one to many relationship as one trek can have multiple bookings but not other side, as one booking can belong to a single trek 


class Booking(db.Model):
    __tablename__='booking'
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id             = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_date        = db.Column(db.DateTime, default=db.func.now())
    booking_status      = db.Column(Enum('booked','cancelled','completed',name='booking_status'), nullable=False, default='booked')   # booked | cancelled | completed
    payment_status      = db.Column(Enum('unpaid','partial','paid','refunded',name='payment_status'), nullable=False, default='unpaid')   # unpaid | partial | paid | refunded
    num_participants    = db.Column(db.Integer, default=1)
    total_amount        = db.Column(db.Float, nullable=True)
    amount_paid         = db.Column(db.Float, default=0.0)
    notes               = db.Column(db.Text, nullable=True)
    cancelled_at        = db.Column(db.DateTime, nullable=True)
    cancellation_reason = db.Column(db.Text, nullable=True)
    created_at          = db.Column(db.DateTime, default=db.func.now())
    updated_at          = db.Column(db.DateTime, onupdate=db.func.now())
    
    # a single user can make multiple bookings, but each booking belongs to just one user
    #relationships
    trek=db.relationship('Trek',back_populates='bookings',lazy=True)#one to many relationship #each booking belong to one trek
    user=db.relationship('User',back_populates='bookings',lazy=True)#one to many relationship 









# ONE-TO-ONE (User ↔ Staff_profile)
# ───────────────────────────────────
# User            Staff_profile
# id=1    ←───    user_id=1   (only one profile per user)


# ONE-TO-MANY (User ↔ Bookings)
# ───────────────────────────────────
# User            Booking
# id=1    ←───    user_id=1
#         ←───    user_id=1
#         ←───    user_id=1   (many bookings per user)


# MANY-TO-MANY (User/Staff ↔ Trek)
# ───────────────────────────────────
# User        trek_staff_assignment      Trek
# id=2  ───→  staff_id=2, trek_id=1 ──→ id=1
# id=2  ───→  staff_id=2, trek_id=2 ──→ id=2
# id=3  ───→  staff_id=3, trek_id=1 ──→ id=1


# User
#  |
#  | 1
#  |
#  +---------<
#  |          Booking
#  |
#  |
#  +---------1
#            StaffProfile

# StaffProfile
#       |
#       | >------< many-to-many
#       |
#      Trek
#       |
#       |
#       +------<
#              Booking