# Trek Mate - Trekking Management Application

Trek Mate is a web-based Trekking Management Application developed using Flask. 
The application allows users to browse and book treks, while trek staff can 
manage assigned treks and participants, and administrators can manage the 
overall trekking system.

## 1. Project Overview

The application provides three different types of users:

- **Admin**
- **Trek Staff**
- **Trekker**

Each role has different permissions and functionalities.

The main purpose of the application is to manage treks, bookings, users, 
trek staff, participants and trek progress through a single web application.

## 2. Technologies Used

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy ORM

### Frontend
- HTML
- CSS
- Jinja2 Templates
- Bootstrap
- JavaScript

### Database
- SQLite

### Other Python Libraries
- Werkzeug
- datetime
- os

## 3. User Roles

### Admin

The administrator has complete control over the application.

Admin can:
- View the admin dashboard
- Create new treks
- Update trek details
- Delete treks
- Assign staff to treks
- Manage trek staff(activate/blacklist) or assign them the treks 
- Manage trekkers/users(activate/blacklist)
- Blacklist users and staff
- Activate/deactivate accounts
- View bookings
- Manage trek status

### Trek Staff
Trek staff members are responsible for managing the treks assigned to them.

Staff can:

- View their profile/Edit their profiles
- View assigned treks
- View participants of assigned treks
- View booking information
- Start a trek
- Complete a trek
- Manage trek-related information
A staff member can be assigned to multiple treks.

### Trekker

Trekkers are the users who participate in treks.

They can:
- Register an account
- Login
- View available treks
- Search for treks
- Filter treks by difficulty
- Filter treks by location
- View detailed trek information
- Book a trek
- View their bookings
- Cancel a booking
- View booking details
- View trekking history(if they have completed their treks)
- Edit their profile

## 4. Main Features

### Authentication

The application provides login and registration functionality.

Users are authenticated according to their role:

- Admin
- Trek Staff
- Trekker

Blacklisted or inactive users are prevented from logging into the system.
### Trek Management

Admin can create and manage treks.

A trek contains information such as:

- Trek name
- Description
- Location
- Difficulty
- Duration
- Start date
- End date
- Maximum slots
- Available slots
- Price
- Status
- Trek progress
- Trek image

Trek status can be:

- Open
- Closed

Trek progress can be:

- Upcoming
- Started
- Completed

---

### Trek Staff Assignment

A trek can have multiple staff members assigned to it, and a staff member 
can also be assigned to multiple treks.

This is implemented using a many-to-many relationship through a junction 
table.

---

### Booking Management

Trekkers can book available treks.

A booking contains:

- User
- Trek
- Booking date
- Booking status
- Payment status
- Number of participants(here we are taking that only one user one booking like not for a family)
- Total amount
- Amount paid
- Notes
- Cancellation information

Booking status can be:

- Booked
- Cancelled
- Completed

The number of participants is calculated from bookings.

Cancelled bookings are not counted as active participants.

Available trek slots are updated when a booking is created or cancelled.

for example:

If a trek has:

    Maximum slots = 20

and a user books:

    3 participants

then:

    Available slots = 20 - 3
                    = 17

If the booking is later cancelled, the slots are restored.

---
### Search and Filtering

Trekkers can browse available treks and filter them using:

- Trek name/search
- Difficulty
- Location

Multiple filters can be applied together.

For example:

    Status = Open
    Difficulty = Hard
    Location = Uttarakhand

The application builds the query step-by-step so that all selected filters 
are applied to the same query.

---
### Trek History

Trekkers can view their previous trekking records.

The history keeps booking records for only completed bookings 

---

### Profile Management

Users can view and update their profile information.

Trek staff profiles contain additional information such as:

- Expertise
- Certifications
- Years of experience
- Bio

---
## 5. Database Design

The application uses SQLite with SQLAlchemy ORM.

The major database tables are:

- `User`
- `Staff_profile`
- `Trek`
- `Booking`
- `trek_staff_assignment`

### User - Booking

One user can have multiple bookings.

Therefore:

    User 1 -------- * Booking
Each booking belongs to one user.

---

### Trek - Booking

One trek can have multiple bookings.

Therefore:

    Trek 1 -------- * Booking

Each booking belongs to one trek.

---

### User - Staff Profile

A staff profile belongs to one user.

Therefore:

    User 1 -------- 1 Staff Profile
---

### Trek - Staff

A trek can have multiple staff members, and a staff member can be assigned 
to multiple treks.

Therefore:

    Trek * -------- * Staff Profile

This many-to-many relationship is implemented using:

    trek_staff_assignment

The junction table contains:

- `trek_id`
- `staff_id`
- `assigned_at`
- `role_on_trek`

---
## 6. Database Relationships

The overall relationship structure is:

    User
     |
     | 1
     |
     | *
    Booking
     |
     | *
     |
     | 1
    Trek
     |
     | *
     |
     | *
    Staff Profile

The many-to-many relationship between Trek and Staff Profile is handled 
through the `trek_staff_assignment` junction table.

## 7. Important Application Logic

### Available Slots

When a booking is created:

    available_slots -= num_participants

When a booking is cancelled:

    available_slots += num_participants

This ensures that available slots remain synchronized with active bookings.

---
### Booking Validation

Before creating a booking, the application checks:

1. Whether the trek exists
2. Whether the trek is open
3. Whether slots are available
4. Whether the user has already booked the trek

This prevents invalid or duplicate bookings.

---
### Account Status

Users have an `is_active` field and a blacklist status.

An administrator can deactivate or blacklist a user or staff member.

Inactive/blacklisted accounts cannot login.

---
## 8. Project Structure

A simplified project structure is:

    trekking-management-application/
    │
    ├── application/
    │   ├── app.py
    │   ├── controller.py
    │   └── models.py
    │
    ├── templates/
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── home.html
    │   ├── trekker_dash.html
    │   ├── trek_details.html
    │   ├── booking_details.html
    │   ├── trekker_history.html
    │   ├── staff_profile.html
    │   ├── staff_participants.html
    │   └── ...
    │
    ├── static/
    │   ├── css/
    │   |
    │   └── images/
    │
    ├── database.sqlite3
    │
    └── README.md

---
## 9. How to Run the Application

### Step 1 - Clone the repository

    git clone <repository-url>

### Step 2 - Open the project directory

    cd trekking-management-application

### Step 3 - Create a virtual environment

    python -m venv venv

### Step 4 - Activate the virtual environment

#### macOS/Linux

    source venv/bin/activate

#### Windows

    venv\Scripts\activate

### Step 5 - Install dependencies

    pip install flask flask-sqlalchemy

Install any additional dependencies used by the project.

### Step 6 - Run the application

    python app.py

### Step 7 - Open the application

Open the local Flask URL shown in the terminal, for example:

    http://127.0.0.1:5000/

---

## 10. Security and Validation

The application includes validation and access control such as:

- Role-based access
- Account activation/deactivation
- Blacklist checking
- Duplicate booking prevention
- Trek availability checking
- Booking ownership verification
- Required form fields
- Secure filename handling for uploaded trek images

## 11. Future Improvements

Possible future improvements include:

- Online payment integration
- Email notifications
- Password hashing improvements
- Password reset functionality
- Better role-based authorization decorators
- Trek reviews and ratings
- Maps and location integration
- Advanced reporting and analytics
- Pagination for large tables
- Improved mobile responsiveness

there are some columns defined inside my schema that are still to be used or implements 
- Total amount
- Amount paid
- Notes
- Payment status
- Price(inside the trek)
- blacklist reason(user)
---
## 12. Conclusion

Trek Mate provides a centralized platform for managing trekking activities.

It connects administrators, trek staff and trekkers while handling trek 
creation, staff assignment, bookings, participants, trek progress and 
trekking history.

The project demonstrates the use of Flask, SQLAlchemy ORM, relational 
database design, Jinja templates, HTML/CSS, Bootstrap and role-based 
application functionality.