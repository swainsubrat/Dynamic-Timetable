from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, ResumeForm
from flaskblog.models import Applicants, User, Timetable
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', timetable=1)

@app.route("/timetable")
@login_required
def timetable():
    date_dict = {
        'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6
    }
    day = datetime.now().strftime("%A")
    tt = {
        'd1':Timetable.query.filter_by(day='Monday').first(),
        'd2':Timetable.query.filter_by(day='Tuesday').first(),
        'd3':Timetable.query.filter_by(day='Wednesday').first(),
        'd4':Timetable.query.filter_by(day='Thursday').first(),
        'd5':Timetable.query.filter_by(day='Friday').first(),
        'd6':Timetable.query.filter_by(day='Saturday').first()
    }
    return render_template('timetable.html', title='Timetable', timetable=1, tt = tt, day = day, d_dict=date_dict)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, subject=form.subject.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/apply", methods=['GET', 'POST'])
def apply():
    form = ResumeForm()
    if form.validate_on_submit():
        f = form.resume.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'resumes', filename
        ))
        applicants = Applicants(
            name=form.name.data,
            number=form.number.data,
            email=form.email.data,
            qualification=form.qualification.data,
            resume_filename=filename
        )
        db.session.add(applicants)
        db.session.commit()
        flash('Document uploaded successfully.')
        return redirect(url_for('home'))
    return render_template('apply.html', title='Apply', form=form)


# @app.route("/admin", methods=['GET', 'POST'])
# def admin():
#     form = RetrieveForm()
