from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, TextField
from wtforms.validators import InputRequired, Length


class AddForm(FlaskForm):

    name = TextField('Name of the Student: ', validators=[InputRequired()])

    surname = TextField('Surname: ', validators=[InputRequired()])

    school_number = IntegerField('Enter the School Number: ', validators=[
                                 InputRequired()])

    add_teacher = SelectField('Choose Your Guidance Teacher: ', choices=[('Jane Smith', 'Jane Smith'), (
        'Anna Charlotte', 'Anna Charlotte'), ('Emma Addison', 'Emma Addison'), ('Abraham Harper', 'Abraham Harper')], validators=[InputRequired()])

    add_branch = SelectField('Select Your Branch: ', choices=[(
        'Law', 'Law'), ('Medicine', 'Medicine'), ('Art', 'Art'), ('Science', 'Science')], validators=[InputRequired()])

    img_url = TextField('Image Url', validators=[InputRequired()])

    submit = SubmitField('Submit')


class DelForm(FlaskForm):

    id = IntegerField('Id number of Student to Remove: ')
    submit = SubmitField('Remove Student')
