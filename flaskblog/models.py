from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Applicants(db.Model, UserMixin):
    '''
    The Applicants table in which the applicants data is stored
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    qualification = db.Column(db.String(20), unique=True, nullable=False)
    resume_filename = db.Column(db.String(60), nullable=False)


class User(db.Model, UserMixin):
    '''
    The User table in which the user data is stored
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    subject = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.subject}')"


class Timetable(db.Model):
    '''
    The timetable table from which current time table will be fetched
    '''
    day = db.Column(
        db.String(20), primary_key=True, unique=True, nullable=False
    )
    p1 = db.Column(db.String(20), unique=False, nullable=True)
    p2 = db.Column(db.String(20), unique=False, nullable=True)
    p3 = db.Column(db.String(20), unique=False, nullable=True)
    p4 = db.Column(db.String(20), unique=False, nullable=True)
    p5 = db.Column(db.String(20), unique=False, nullable=True)
    p6 = db.Column(db.String(20), unique=False, nullable=True)
    p7 = db.Column(db.String(20), unique=False, nullable=True)
    p8 = db.Column(db.String(20), unique=False, nullable=True)
    p9 = db.Column(db.String(20), unique=False, nullable=True)

    def __repr__(self):
        return f"Day: {self.day}, P1: {self.p1}, P2: {self.p2}, P3: {self.p3},\
        P4: {self.p4}, P5: {self.p5}, P6: {self.p6}, P7: {self.p7}, \
        P8: {self.p8}, P9: {self.p9}"
