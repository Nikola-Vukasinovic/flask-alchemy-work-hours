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
        existing_entry = Entry.query.filter_by(user_id=current_user.id, date=form.date.data).first()
        
        if existing_entry:
            flash('You already have an entry for this date.', 'danger')
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


@entries.route('/view_entries', methods=["POST", "GET"])
@login_required
def view_entries():
    """Display entries for the current user or selected user if admin, based on selected month """
     # Default to the current month and year
    year = request.form.get('year', date.today().year)
    month = request.form.get('month', date.today().month)
    
    if current_user.is_admin:
        # If admin, get selected user and month from form data
        selected_user_id = request.form.get('user_id', current_user.id)
        month = request.form.get('month', date.today().month)

    # Convert year and month to integers
    year = int(year)
    month = int(month)
    
    # Get the first and last day of the month as date objects
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    
    # Query entries for the selected month
    entries = Entry.query.filter(
        Entry.user_id == current_user.id,
        Entry.date >= first_day,
        Entry.date <= last_day
    ).all()

    #Query all the users
    users = User.query.all()  # Get all users for the dropdown if admin
    # Calculate total hours
    total_hours = sum(entry.hours for entry in entries)
    
    return render_template('entries/view_entries.html', entries=entries, year=year, month=month, today=date.today(), total_hours=total_hours, users=users)


@entries.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    
    if entry.user_id != current_user.id:
        flash('You are not authorized to edit this entry.', 'danger')
        return redirect(url_for('core.index'))
    
    form = EntryForm(obj=entry)  # Assuming you have an EntryForm for editing

    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('entries.view_entries'))
    
    return render_template('entries/edit_entry.html', form=form, entry=entry)


