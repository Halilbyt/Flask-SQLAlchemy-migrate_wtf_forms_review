import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm, DelForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'somesecretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Database section
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    sch_id = db.Column(db.Integer)
    img_url = db.Column(db.Text)

    # One to One relationship
    branch = db.relationship(
        'Branch', backref='student', uselist=False)
    teacher = db.relationship(
        'Teacher', backref='student', uselist=False)

    def __init__(self, name, surname, sch_id, img_url):
        self.name = name
        self.surname = surname
        self.sch_id = sch_id
        self.img_url = img_url

    def __repr__(self):
        if self.branch or self.teacher:
            return f"Student Id: {self.id} \n Name: {self.name} Surname: {self.surname} \nGuidance Teacher: {self.teacher.name_surname}\n Branch: {self.branch.branch_name}"
        else:
            return f"Student Id: {self.id} \n Name: {self.name} Surname: {self.surname} \nGuidance Teacher: No teacher selected\n Branch: No Branch selected"


class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name_surname = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, name_surname, student_id):
        self.name_surname = name_surname
        self.student_id = student_id

    def __repr__(self):
        return f"Name of Guidance Teacher: {self.name_surname}"


class Branch(db.Model):

    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, branch_name, student_id):
        self.branch_name = branch_name
        self.student_id = student_id

    def __repr__(self):
        return f"Branch Name: {self.branch_name}"

# Web route parts


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/add', methods=['GET', 'POST'])
def add_std():
    form = AddForm()

    if form.validate_on_submit():

        name = form.name.data
        surname = form.surname.data
        school_id = form.school_number.data
        teacher = form.add_teacher.data
        branch = form.add_branch.data
        url = form.img_url.data

        new_student = Student(name=name, surname=surname,
                              sch_id=school_id, img_url=url)
        db.session.add(new_student)
        db.session.commit()

        new_student_id = Student.query.filter_by(
            name=new_student.name).first().id

        # print("_______________________________")
        # print("New Student id:", new_student.id)
        # print("teacher: ", teacher)
        # print("branch: ", branch)
        # print("_______________________________")

        new_branch = Branch(branch, new_student_id)
        db.session.add(new_branch)
        db.session.commit()

        new_teacher = Teacher(teacher, new_student_id)
        db.session.add(new_teacher)
        db.session.commit()

        return redirect(url_for('listing_student'))

    return render_template('add.html', form=form)


@app.route('/students')
def listing_student():
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/delete', methods=['GET', 'POST'])
def delete_std():

    form = DelForm()

    if form.validate_on_submit():
        try:
            id = form.id.data
            get_student = Student.query.get(id)
            db.session.delete(get_student)
            db.session.commit()

            return redirect(url_for('listing_student'))
        except Exception as e:
            return render_template('error.html', error=e)

    return render_template('delete.html', form=form)


if __name__ == '__main__':
    app.run()


"""
    class Owner(db.Model):
    ...
    ...
    ...
    Quick Tutorial about one to many relationship
    # First argument is the name of the class in a string
    # Backref meaning new column basically on the child 
    pets = db.relationship('pet',backref='owner')

    class Pet(db.Model)
    ...
    ...
    ...
    owner_id = db.Column(db.Integer,db.ForeignKey('owner.id'))  

    many to many relationship tutorial:

"""
