from datetime import datetime
from imdb_webapp import db,login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#User Table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(20),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    image_file= db.Column(db.String(20),nullable=False,default='default.jpg')
    password= db.Column(db.String(60), nullable=False)
    comments = db.relationship('Comment', backref='author', lazy=True)
    

    def _repr_(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
#Movie Table
class Movie(db.Model):
    __searchable__=['title']
    id=db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(50),unique=True,nullable=False)
    year= db.Column(db.String(50),nullable=False)
    director= db.Column(db.String(50),nullable=False)
    star= db.Column(db.String(150),nullable=False)
    genre= db.Column(db.String(50),nullable=False)
    runtime= db.Column(db.String(50),nullable=False)
    description= db.Column(db.Text,nullable=False)
    prediction= db.Column(db.String(50))
    image_movie= db.Column(db.String(20),nullable=False,default='default.jpg')
    Recommended1=db.Column(db.String(50))
    Recommended2=db.Column(db.String(50))
    Recommended3=db.Column(db.String(50))
    Recommended4=db.Column(db.String(50))
    Recommended5=db.Column(db.String(50))
    
    

    def _repr_(self):
        return f"User('{self.title}','{self.year}',' {self.director}','{self.star}','{self.genre}','{self.runtime}','{self.image_movie}')"

#Comment Table
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   

    def __repr__(self):
        return f"Comment('{self.date_posted}')"    

#Actor Table
class Actor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(50),unique=True,nullable=False)
    gender= db.Column(db.String(50),nullable=False)
    born= db.Column(db.String(50),nullable=False)
    movies= db.Column(db.String(150),nullable=False)
    place= db.Column(db.String(50),nullable=False)
    description= db.Column(db.Text,nullable=False)
    image_actor= db.Column(db.String(20),nullable=False,default='default.jpg')
    
    

    def _repr_(self):
        return f"User('{self.name}','{self.gender}',' {self.born}','{self.movies}','{self.place}','{self.image_actor}')"
    
    