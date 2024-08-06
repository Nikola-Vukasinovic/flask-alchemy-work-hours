from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from work_hours_app import db
from work_hours_app.models import User, Entry
from work_hours_app.users.forms import LoginForm, RegisterForm, UpdateUserForm, AddUserForm
from work_hours_app.entries.forms import EntryForm

from datetime import datetime, date
from calendar import monthrange

entries = Blueprint("entries", __name__)


@entries.route("/add_hours", methods=["POST", "GET"])
@login_required
def add_hours():
    """Add hours for current month"""
    form = EntryForm()

    if form.validate_on_submit():
        #existing_entry = Entry.query.filter_by(user_id=current_user.id, date=form.date.data).first()
        existing_entry = Entry.query.filter_by(user_id=current_user.id).first()
        print(current_user.id)
        print(form.date.data)
        print(existing_entry)
        if existing_entry:
            flash('You already have an entry for this date.', 'warning')
        else:
            entry = Entry(
                user_id=current_user.id,
                date=form.date.data,
                description=form.description.data,
                hours=form.hours.data,
                time_start=form.time_start.data,
                time_end=form.time_end.data
            )
            db.session.add(entry)
            db.session.commit()
            flash('Hours added successfully!', 'success')
            return redirect(url_for('entries.view_entries'))

    return render_template('entries/add_hours.html', form=form)


@entries.route('/view_entries')
@login_required
def view_entries():
    """ Return all of the entries for current month and current user """
    today = date.today()
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month, monthrange(today.year, today.month)[1])

    # Query the database for entries for the current month for the logged-in user
    entries = Entry.query.filter(
        Entry.user_id == current_user.id,
        Entry.date >= start_date,
        Entry.date <= end_date
    ).all()

    return render_template('entries/view_entries.html', entries=entries, current_date=today)