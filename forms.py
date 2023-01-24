
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


app = Flask(__name__)
class AddLinkForm(FlaskForm):
    #newlink = StringField('')
    def hello(self):
        return "hello world"
    newrss = StringField('New Rss', validators=[DataRequired()])
    submit = SubmitField('Submit')







