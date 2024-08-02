from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from work_hours_app import db
from work_hours_app.models import User, Entry
from work_hours_app.users.forms import LoginForm, RegisterForm, UpdateUserForm, AddUserForm

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    """ Login user view """
    form = LoginForm()
    
    if form.validate_on_submit():
        user_input = form.username_or_email.data
        user = None

        if '@' in user_input:
            user = User.query.filter_by(email=user_input).first()
        else:
            user = User.query.filter_by(username=user_input).first()
        
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Login was Success!", "success")

            next = request.args.get("next")

            if next == None or not next.startswith("/"):
                next = url_for("core.index")

            return redirect(next)
        else:
            flash("Invalid username/email or password", "danger")
    
    return render_template("users/login.html", form=form)
    

@users.route("/logout")
def logout():
    """ Logout user view """
    logout_user()
    flash("Logout was Success!", "success")
    return redirect(url_for("core.index"))


@users.route("/management")
def management():
    """ Manage users """
    pass

@users.route("/register", methods=["POST", "GET"])
@login_required
def register():
    if current_user.is_admin:

        form = AddUserForm()

        if form.validate_on_submit():
            user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    is_admin = form.is_admin.data)
            
            db.session.add(user)
            db.session.commit()
            flash("User has been added successfully.", "success")
            return redirect(url_for("core.index"))
        
    return render_template("users/register.html", form=form)


@users.route("/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():
    if not current_user.is_admin:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("core.index"))

    users = User.query.all()

    # Handle the editing of user information
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user = User.query.get_or_404(user_id)

        # Update user details
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.firstname = request.form.get("firstname")
        user.lastname = request.form.get("lastname")
        user.is_admin = 'is_admin' in request.form  # Check if the admin checkbox is checked

        db.session.commit()
        flash("User information updated successfully!", "success")
        return redirect(url_for("users.manage_users"))

    return render_template("users/manage_users.html", users=users)

   

@users.route("/update_user/<int:user_id>", methods=["POST"])
@login_required
def update_user(user_id):
    """Update an existing user."""
    if not current_user.is_admin:
        flash("You do not have permission to update users.", "danger")
        return redirect(url_for("core.index"))

    user = User.query.get_or_404(user_id)

    user.username = request.form['username']
    user.email = request.form['email']
    user.firstname = request.form['firstname']
    user.lastname = request.form['lastname']
    user.is_admin = 'is_admin' in request.form  # Check if the checkbox was checked

    db.session.commit()
    flash("User information updated successfully!", "success")
    return redirect(url_for("users.manage_users"))


@users.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    """Delete a user."""
    if not current_user.is_admin:
        flash("You do not have permission to delete users.", "danger")
        return redirect(url_for("core.index"))

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    
    flash(f"User '{user.username}' has been deleted successfully!", "success")
    return redirect(url_for("users.manage_users"))