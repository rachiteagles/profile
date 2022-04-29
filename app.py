import os

from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired,InputRequired
import smtplib
from lib.catNdog import predict

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY=os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sway.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key

# Initialization
# Create an application instance (an object of class Flask)  which handles all requests.
app = Flask(__name__)
app.config.from_object(Config)

class Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def mail(name,email,message):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login("rachit1405@gmail.com", "oijzoycmrwddnbzg")

    # message to be sent
    subject=name+' '+email
    content=message
    message = f"Subject: {subject}\n{content}"
    
    # sending the mail
    s.sendmail("rachit1405@gmail.com", "rachit1405@gmail.com", message)
    
    # terminating the session
    s.quit()

@app.route('/', methods=('GET', 'POST'))
def index():
    



    form = Form()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        try:
            mail(name=name,email=email,message=message)
            flash('Message send!')
        except:
            flash('Error in sending mail')

    return render_template('index.html',form=form)

@app.route('/catNdog_demo', methods=('GET', 'POST'))
def catNdog():
    catNdog_form = UploadFileForm()
    if catNdog_form.validate_on_submit():
        file = catNdog_form.file.data # First grab the file

        
        if predict(file) == 0:
            flash("It is a Cat")
        else:
            flash("It is a Dog")


    form = Form()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        try:
            mail(name=name,email=email,message=message)
            flash('Message send!')
        except:
            flash('Error in sending mail')
    return render_template('catNdog_demo.html', form=form, catNdog_form=catNdog_form)


if __name__ == '__main__':
    app.run(debug=True)