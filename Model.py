from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eSeed.db'


db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    hireDate = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '%r' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),
                            nullable=False)
    employee = db.relationship('Employee',
                               backref=db.backref('User', lazy=True))

    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '%r' % self.id


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    present = db.Column(db.Boolean, unique=False)
    absent = db.Column(db.Boolean, unique=False)
    sick_Leave = db.Column(db.Boolean, unique=False)
    day_OFF = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        return '%r' % self.id


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    Day = db.Column(db.String(20), unique=False, nullable=False)
    Working_hours = db.Column(db.Integer, unique=False, nullable=False)


    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),
                        nullable=False)
    employee = db.relationship('Employee',
                           backref=db.backref('Attendance', lazy=True))

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'),
                            nullable=False)
    status = db.relationship('Status',
                               backref=db.backref('Attendance', lazy=True))

    def __repr__(self):
        return '%r' % self.id


if __name__ == '__main__':
   # db.create_all()
   #  employee = Employee(name = "MustafaArafa", email = 'Mustafa@gmail.com', mobile_no = '01113600147',
   #               hireDate ='10/10/2017' )
    status = Status( present = True, absent = False, sick_Leave = False, day_OFF = False)
    #user = User(password = "nnnnn", employee=employee)
    #att = Attendance( Day =datetime.strptime( datetime.today().strftime('%Y-%m-%d')), Working_hours =7, employee=employee, status=status)
    att = Attendance( Day =datetime.today().strftime('%Y-%m-%d'), Working_hours =7, employee_id=2, status=status)

    # db.session.add(employee)
    db.session.add(status)
    db.session.commit()