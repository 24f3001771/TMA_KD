from .database import db  #.database means current folder

#assosiation or junction table (relationship table between staff and trek (many-to-many))
trek_staff_assignment = db.Table("trek_staff_assignment",
    db.Column('trek_id', db.Integer , db.Foreignkey('Trek.id'),primary_key=True),
    db.Column('staff_id', db.Integer , db.ForeignKey('Staff_profile.id',primary_key=True)),
    db.Column('assigned_at',db.DateTime, default=db.func.now()),
    db.Column('role_on_trek',db.String(),nullable=True)
    )


class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    email=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    full_name        = db.Column(db.String(), nullable=True)
    phone            = db.Column(db.String(), nullable=True)
    role=db.Column(db.String(),nullable=False,default='trekker')
    is_blacklisted=db.Column(db.Boolean,default=False)
    blacklist_reason=db.Column(db.Text,nullable=True)
    is_active=db.Column(db.Boolean,default=True)
    created_at       = db.Column(db.DateTime, default=db.func.now())
    updated_at       = db.Column(db.DateTime, onupdate=db.func.now())

    #Relationships
    bookings=db.relationship('Booking',lazy=True, back_populates='user')
    staff_profile=db.relationship('Staff_profile',lazy=True,uselist=False,back_populates='user') #uselist= False means One-to-one (single object) while default it is one-to-many


class Staff_profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('User.id'),unique=True,nullable=False)
    contact_details=db.Column(db.String(),nullable=True)
    bio=db.Column(db.Text,nullable=True)
    expertise=db.Column(db.String(),nullable=True)
    certifications   = db.Column(db.Text, nullable=True)
    years_experience = db.Column(db.Integer, nullable=True)
    approval_status  = db.Column(db.String(), nullable=False, default='pending')  # pending | approved | blacklisted
    is_available     = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime,default=db.func.now())
    updated_at = db.Column(db.DateTime,default=db.func.now())

    #Relationships
    assigned_treks=db.relationship('Trek',secondary='trek_staff_assignment',lazy=True,back_populates='assigned_staffs')
    user=db.relationship('User',back_populates='staff_profile',lazy=True)


class Trek(db.Model):
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
    price           = db.Column(db.Float, nullable=False, default=0.0)
    status          = db.Column(db.String(), nullable=False, default='pending')  # pending | approved | open | closed | completed | cancelled
    created_at      = db.Column(db.DateTime, default=db.func.now())
    updated_at      = db.Column(db.DateTime, onupdate=db.func.now())
    

    #Relationships
    assigned_staffs=db.relationship('Staff_profile',secondary='trek_staff_assignment',lazy=True,back_populates='assigned_treks')
    booking=db.relationship('Booking',back_populates='assigned_treks',lazy=True)


class Booking(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    trek_id             = db.Column(db.Integer, db.ForeignKey('Trek.id'), nullable=False)
    booking_date        = db.Column(db.DateTime, default=db.func.now())
    booking_status      = db.Column(db.String(), nullable=False, default='booked')   # booked | cancelled | completed
    payment_status      = db.Column(db.String(), nullable=False, default='unpaid')   # unpaid | partial | paid | refunded
    num_participants    = db.Column(db.Integer, default=1)
    total_amount        = db.Column(db.Float, nullable=True)
    amount_paid         = db.Column(db.Float, default=0.0)
    notes               = db.Column(db.Text, nullable=True)
    cancelled_at        = db.Column(db.DateTime, nullable=True)
    cancellation_reason = db.Column(db.Text, nullable=True)
    created_at          = db.Column(db.DateTime, default=db.func.now())
    updated_at          = db.Column(db.DateTime, onupdate=db.func.now())
    

    #relationships
    assigned_treks=db.relationship('Trek',back_populates='booking',lazy=True)
    user=db.relationship('User',back_populates='bookings',lazy=True)

