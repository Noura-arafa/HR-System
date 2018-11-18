from flask import Flask, request, render_template, url_for, flash, redirect
from sqlalchemy import create_engine
from Forms import LogInForm, UpdateForm, DeleteForm
from flask_sqlalchemy import SQLAlchemy
from Model import Employee, User, Status, Attendance
from datetime import datetime

db_connect = create_engine('sqlite:///eSeed.db')
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eSeed.db'
app.config['SECRET_KEY'] = '5916235cc06905ed364ba43b11005efd'
#api = Api(app)
db = SQLAlchemy(app)

@app.route("/system", methods=["GET"])
def system():
    return render_template('system.html')


@app.route("/login", methods=["GET","POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()

        if employee:
            user = User.query.filter_by(employee_id=employee.id).first()
            if user.password == form.password.data:
                flash(f'Welcome!', category='success')
                # this will go to home fun home here is fun_name not route name
                return redirect(url_for('system'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route('/Employees')
def get_employees():
    conn = db_connect.connect()
    query = conn.execute("select * from employee ")
    employees = query.fetchall();
    attendens = []
    status = []
    for employee in employees:
        #query = conn.execute("select * from attendence where employee_id = '%d' AND Day = '%s' ", (int(employee.id)), datetime.today())
        employee_attendance = conn.execute("""
              select * from attendance where Day = ? AND employee_id = ?
           """, (datetime.today().strftime('%Y-%m-%d')), int(employee.id)).cursor.fetchone()
        attendens.append(employee_attendance)
        statu = conn.execute("select * from status where id = '%d'" % int(employee_attendance[4])).cursor.fetchone()
        status.append(statu)
    print(employees)
    print(attendens)
    print(status)
    return render_template('employees.html', employees=employees, attendens=attendens, status=status)


@app.route('/deleteEmployee', methods=['GET'])
def deleteEmployee():
    conn = db_connect.connect()
    form = DeleteForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(id=form.employeeID.data).first()
        print(employee)
        if employee:
            db.session.delete(employee)
            db.session.commit()
    return render_template('deleteEmployee.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = db_connect.connect()
    form = UpdateForm()
    if form.validate_on_submit():
        print('heeeeer')
        employee = Employee.query.filter_by(id=form.employeeID.data).first()
        print(employee)
        if employee:

            status = Status(present=form.present.data, absent=form.absent.data, sick_Leave=form.sickLeave.data,
                            day_OFF=form.dayOFF.data)
            att = Attendance(Day=datetime.today().strftime('%Y-%m-%d'), Working_hours=form.workingHours.data,
                             employee_id=form.employeeID.data, status=status)
            db.session.add(status)
            db.session.commit()

            return redirect(url_for('system'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('manageEmployee.html',  form=form)


if __name__ == '__main__':
    app.run()
