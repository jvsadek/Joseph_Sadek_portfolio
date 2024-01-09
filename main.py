from flask import Flask, abort, render_template, redirect, url_for, flash, request, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SubmitField, PasswordField
from flask_ckeditor import CKEditor, CKEditorField
import os

app = Flask(__name__)
app.config['SECRET_KEY']=  os.environ.get('FLASK_KEY')
# app.config['SECRET_KEY']= '$2y$10$pDdusVebcpKMV0t2FkVr0eui6/9JInSSW31kkcbqm6zLY1LiqwNxG'
ckeditor = CKEditor(app)
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///messages.db")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'


db = SQLAlchemy()
db.init_app(app)

# Create a User table for all your registered users
class Contact(db.Model):
    __tablename__ = "Contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    subject = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit!")


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def main_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(Contact).where(Contact.email == form.email.data))
        user = result.scalar()
        if  user:
            # User already send message
            flash("You've already sent me a message, I will get back ASAP!")
            return redirect(url_for('main_page'))
            # render_template("index.html", form=form)
        else:
            # User already send message
            flash("Thank you for your message, I will get back ASAP!")
            # return redirect(url_for('main_page'))
            new_message = Contact(
                email=form.email.data,
                name=form.name.data,
                subject = form.subject.data,
                message = form.message.data,
            )
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for("main_page"))

    return render_template("index.html", form=form)

@app.route('/download')
def download_resume():
    return send_from_directory('static', path="./files/Resume-Joseph-Sadek_2024.pdf")

if __name__ == "__main__":
    app.run(debug=False, port=5001)