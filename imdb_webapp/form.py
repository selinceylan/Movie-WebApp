from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed 
from flask_login import current_user 
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError 
from imdb_webapp.models import User


class RegistrationForm(FlaskForm):
    
    #Username-check not empty and length is between 2 to 20
    username=StringField('Username',
                        validators=[DataRequired(), Length(min=2,max=20)])
    #Email-check not empty and be sure it is email
    email=StringField('Email',
                        validators=[DataRequired(),Email()])
    #Password
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])   
    #Submit 
    submit=SubmitField('Sign Up')    

    #Check username is unique or not
    def validate_username (self,username):
        user=User.query.filter_by(username=username.data).first()
        if user: 
           raise ValidationError("That username is taken.Please choose a different one.")        

    #Check email is unique or not
    def validate_email (self,email):
        user=User.query.filter_by(email=email.data).first()
        if user: 
           raise ValidationError("That email is taken.Please choose a different one.")        

class LoginForm(FlaskForm):
    
    #Email-check not empty and be sure it is email
    email=StringField('Email',
                        validators=[DataRequired(),Email()])
    #Password
    password=PasswordField('Password',validators=[DataRequired()])
    #Remember
    remember=BooleanField('Remember Me')
   #Submit 
    submit=SubmitField('Login')              

class UpdateAccountForm(FlaskForm):
    
    #Username-check not empty and length is between 2 to 20
    username=StringField('Username',
                        validators=[DataRequired(), Length(min=2,max=20)])
    #Email-check not empty and be sure it is email
    email=StringField('Email',
                        validators=[DataRequired(),Email()])
   
    #Update profile picture
    picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    #Submit 
    submit=SubmitField('Update')    

    #Check username is unique or not
    def validate_username (self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError("That username is taken.Please choose a different one.")        

    #Check email is unique or not
    def validate_email (self,email):

        if email.data != current_user.email:
             user=User.query.filter_by(email=email.data).first()
             if user: 
                raise ValidationError("That email is taken.Please choose a different one.")        

class MovieForm(FlaskForm):
    picture= FileField('Update Movie Picture', validators=[FileAllowed(['jpg','png'])])
    title= StringField('Title',validators=[DataRequired()])
    genre=StringField('Genre',validators=[DataRequired()])
    runtime=StringField('Runtime',validators=[DataRequired()])
    year=StringField('Year',validators=[DataRequired()])
    actors=StringField('Actors',validators=[DataRequired()])
    director=StringField('Director',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    #Update profile picture
    picture= FileField('Update Movie Picture', validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Post')

class SearchForm(FlaskForm):
    
    select= SelectField('Search for movie:')
    search=StringField('')

class ActorForm(FlaskForm):
    picture= FileField('Update Actor Picture', validators=[FileAllowed(['jpg','png'])])
    name= StringField('Name and Surname',validators=[DataRequired()])
    gender=StringField('Gender',validators=[DataRequired()])
    born=StringField('Born',validators=[DataRequired()])
    movie=StringField('Movie(s)',validators=[DataRequired()])
    place=StringField('Place of Birth',validators=[DataRequired()])
    content=TextAreaField('About Her/Him',validators=[DataRequired()])
    #Update profile picture
    picture= FileField('Update Actor Picture', validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Post')

class CommentForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit= SubmitField('Comment')   