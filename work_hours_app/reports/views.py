from flask import render_template, url_for,flash, redirect, request, Blueprint, send_file
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func

import pandas as pd

from openpyxl import Workbook
from io import BytesIO
from weasyprint import HTML
from fpdf import FPDF

from work_hours_app import db
from work_hours_app.models import User, Entry
from work_hours_app.users.forms import LoginForm, RegisterForm, UpdateUserForm, AddUserForm
from work_hours_app.entries.forms import EntryForm

from datetime import datetime, date
from calendar import monthrange

reports = Blueprint("reports", __name__)


@reports.route("/report", methods=["POST", "GET"])
@login_required
def report():
    """Report hours based on user id and month"""
    # Default values
    year = date.today().year
    month = date.today().month
    selected_user_id = current_user.id

    if request.method == 'POST':
        if current_user.is_admin:
            selected_user_id = request.form.get('user_id', current_user.id)
            month = int(request.form.get('month', date.today().month))

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

    return render_template('reports/report.html', entries=entries, users=users, year=year, month=month, selected_user_id=selected_user_id, today=date.today(), total_hours=total_hours)


@reports.route('/export/xlsx/<int:user_id>/<int:month>', methods=['GET'])
@login_required
def export_xlsx(user_id, month):
    user = User.query.get(user_id)
    entries = Entry.query.filter(
        Entry.user_id == user_id,
        func.extract('month', Entry.date) == month
    ).all()
    
    # Create a DataFrame from the entries
    data = {
        'Date': [entry.date for entry in entries],
        'Description': [entry.description for entry in entries],
        'Hours': [entry.hours for entry in entries],
        'Time Start': [entry.time_start for entry in entries],
        'Time End': [entry.time_end for entry in entries],
    }
    
    df = pd.DataFrame(data)
    
    # Calculate total hours
    total_hours = df['Hours'].sum()

    # Append total hours as a new row
    total_row = pd.DataFrame({
        'Date': ['Total'],
        'Description': [''],
        'Hours': [total_hours],
        'Time Start': [''],
        'Time End': ['']
    })
    df = pd.concat([df, total_row], ignore_index=True)

    # Create a BytesIO stream for the Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Work Entries')
    
    output.seek(0)

    # Filename format: username_lastname_firstname_month.xlsx
    filename = f"{user.username}_{user.lastname}_{user.firstname}_month_{month}.xlsx"

    # Update send_file to use download_name instead of attachment_filename
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@reports.route('/export/pdf', methods=['GET', 'POST'])
@login_required
def export_pdf():
    selected_user_id = request.args.get('user_id', current_user.id)
    user = User.query.get(selected_user_id)
    month = request.args.get('month', date.today().month)
    entries = Entry.query.filter(
        Entry.user_id == selected_user_id,
        func.extract('month', Entry.date) == month
    ).all()

    # Calculate total hours
    total_hours = sum(entry.hours for entry in entries)

    html = render_template('reports/pdf_template.html', entries=entries, total_hours=total_hours)
    
    filename = f"{user.username}_{user.lastname}_{user.firstname}_month_{month}.pdf"
    
    pdf = HTML(string=html).write_pdf()

    return send_file(BytesIO(pdf), as_attachment=True, download_name=filename, mimetype="application/pdf")