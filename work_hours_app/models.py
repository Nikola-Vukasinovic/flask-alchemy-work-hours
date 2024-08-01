from work_hours_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, index = True)
    name = db.Column(db.String(80), nullable = True)
    lastname = db.Column(db.String(80), nullable = True)
    password_hash = db.Column(db.String(128), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = True)
    is_admin = db.Column(db.Boolean, default = False)

    entries = db.relationship("Entry", backref = "author", lazy = True)

    def __init__(self, username, password, email = None, is_admin = False, name = None, lastname = None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.is_admin = is_admin
        self.name = name
        self.lastname = lastname

    def __repr__(self):
        return f"User is: {self.username} with email: {self.email} is admin: {self.is_admin}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Entry(db.Model):
    __tablename__ = "entries"

    users = db.relationship(User)
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    description = db.Column(db.String(250), nullable = True)
    hours = db.Column(db.Integer, nullable = False)
    time_start = db.Column(db.Time, nullable = True)
    time_end = db.Column(db.Time, nullable = True)

    def __init__(self, date, description, hours, time_start = None, time_end = None):
        self.date = date
        self.description = description
        self.hours = hours
        self.time_start = time_start
        self.time_end = time_end

    def __repr__(self):
        return f"Entry ID: {self.id} -- User ID: {self.user_id} -- Date: {self.date} -- Hours: {self.hours} -- Description: {self.description}"
    