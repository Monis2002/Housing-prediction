from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class Take_data(FlaskForm):
    budget=StringField("Budget in Lakh", validators=[DataRequired()])
    BHK=StringField("BHK",validators=[DataRequired()])
    submit=SubmitField("Search")

