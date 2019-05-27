from flask import render_template,flash,redirect,request,abort
from flask import url_for
import secrets
import os
from PIL import Image
import flask_whooshalchemy as wa
from imdb_webapp import db
from imdb_webapp import app,bcrypt
from imdb_webapp.form import RegistrationForm,LoginForm, UpdateAccountForm, MovieForm, ActorForm, CommentForm,SearchForm
from imdb_webapp.models import User,Movie,Actor,Comment
from flask_login import login_user,current_user,logout_user,login_required
from flask import request

wa.whoosh_index(app,Movie)

#HOME PAGE
@app.route("/")
@app.route("/home")
@app.route("/post/home")
def home():
    return render_template('home.html')

#ACTOR PAGE
@app.route("/")
@app.route("/actor")
@app.route("/post/actor")
def actor():
    return render_template('home_actor.html')



#REGISTER PAGE
@app.route("/register",methods=['GET','POST'])
@app.route("/post/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    #If submit is success print alert message
    if form.validate_on_submit():
        #HASH PASSWORD
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #ADD USER TO DATABASE
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

#LOGIN PAGE
@app.route("/login",methods=['GET','POST'])
@app.route("/post/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form=LoginForm()
     #check email and password if it is true go home page
    if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful.Please check email and password','danger')


    return render_template('login.html',title='Login',form=form)

#LOG OUT
@app.route("/logout")
@app.route("/post/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path= os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)

    #Resize the image
    output_size=(100,100)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#ACCOUNT
@app.route("/account",methods=['GET','POST'])
@app.route("/post/account",methods=['GET','POST'])
@login_required
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            if form.picture.data:
                picture_file=save_picture(form.picture.data)
                current_user.image_file=picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file= url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

#SHOW ALL MOVIES
@app.route("/movie_home",methods=['GET','POST'])
@app.route("/post/movie_home",methods=['GET','POST'])
def movie_home():
    page=request.args.get('page',1,type=int)
    movies=Movie.query.paginate(page=page,per_page=20)
    return render_template('movie_home.html',posts=movies)

#ADD MOVIE
@app.route("/new_movie",methods=['GET','POST'])
@app.route("/post/new_movie",methods=['GET','POST'])
@login_required
def new_movie():
    form=MovieForm()
    if form.validate_on_submit():
        movie=Movie(title=form.title.data,genre=form.genre.data,runtime=form.runtime.data,year=form.year.data,star=form.actors.data,director=form.director.data,description=form.content.data)
        db.session.add(movie)
        db.session.commit()
        flash('Your movie post has been created!','success')
        return redirect(url_for('movie_home'))

    return render_template('create_movie.html',title='New Movie',form=form,legend='New Movie')


#SHOW MOVIE INFO
@app.route("/post/<int:movie_id>", methods=['GET','POST'])
def movie(movie_id):
    form=CommentForm()
    posts=Comment.query.all()
    movie=Movie.query.get_or_404(movie_id)
    if form.validate_on_submit():
        post=Comment(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your comment has been created!','success')
        return redirect(url_for('movie',movie_id=movie.id))
    
    return render_template('movie_info.html',title=movie.title,year=movie.year,runtime=movie.runtime,
                            genre=movie.genre,description=movie.description,director=movie.director,star=movie.star,
                            prediction=movie.prediction,image_movie=movie.image_movie,
                            Recommended1=movie.Recommended1,Recommended2=movie.Recommended2,Recommended3=movie.Recommended3,
                            Recommended4=movie.Recommended4,Recommended5=movie.Recommended5,post=movie,movie_id=movie.id,form=form,posts=posts)

#UPDATE MOVIE
@app.route("/post/<int:movie_id>/update",methods=['GET','POST'])
def update_movie(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    form=MovieForm()
    if form.validate_on_submit():
        movie.title=form.title.data
        movie.genre=form.genre.data
        movie.runtime=form.runtime.data
        movie.year=form.year.data
        movie.star=form.actors.data
        movie.director=form.director.data
        movie.description=form.content.data
        db.session.commit()
        flash('Your post has been update!','success')
        return redirect(url_for('movie',movie_id=movie.id))
    elif request.method=='GET':
        form.title.data=movie.title
        form.genre.data=movie.genre
        form.runtime.data=movie.runtime
        form.year.data=movie.year
        form.actors.data=movie.star
        form.director.data=movie.director
        form.content.data=movie.description
    return render_template('create_movie.html',title='Update Movie',form=form, legend='Update Post',movie_id=movie.id)

#DELETE MOVIE
@app.route("/post/<int:movie_id>/delete",methods=['POST'])
def delete_movie(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit() 
    flash('Your post has been deleted!','success') 
    return redirect(url_for('movie_home'))

 #SHOW RECOMMENDED MOVIE INFO
@app.route("/post/<int:movie_title>")
def title(movie_title):
    movie=Movie.query.get_or_404(movie_title)
    return render_template('movie_info.html',title=movie.title,year=movie.year,runtime=movie.runtime,genre=movie.genre,description=movie.description,director=movie.director,star=movie.star,post=movie,movie_title=movie.title)




#SEARCH
@app.route("/getdb",methods=['POST','GET'])
@app.route("/post/getdb",methods=['POST','GET'])
def getdb():
    if request.method=='POST':
        var=request.form.get('var')
        var = request.form['var']

        look_for = '%{0}%'.format(var)
        log1 = Movie.query.filter(Movie.title.like(look_for))
        return  render_template ('results.html',posts=log1)
    
    return render_template('results.html')

#WATCHLIST
@app.route("/watchlist",methods=['POST','GET'])
@app.route("/post/watchlist",methods=['POST','GET'])
def watchlist():
    return render_template('watchlist.html')
