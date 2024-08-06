from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

from datetime import datetime


class EntryForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    hours = IntegerField('Hours', validators=[DataRequired(), NumberRange(min=0)])
    time_start = TimeField('Start Time', format='%H:%M', validators=[Optional()])
    time_end = TimeField('End Time', format='%H:%M', validators=[Optional()])
    submit = SubmitField('Add Entry')