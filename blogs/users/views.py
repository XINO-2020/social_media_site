#users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blogs import  db
from blogs.models import User,BlogPost
from blogs.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from blogs.users.picture_handler import add_profile_pic
from sqlalchemy import desc

users = Blueprint('users', __name__)
#register.login.logout.acoount.bloglist
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route('/register' , methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(fname = form.fname.data, email=form.email.data,
                    username = form.username.data,
                    password= form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')
        return redirect(url_for('users.login'))

    return render_template('register.htm', form = form)

@users.route('/login',methods=['GET','POST'])
def login():
    error = ''
    if current_user.is_authenticated == False:
        form = LoginForm()
        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if user is not None and user.check_password(form.password.data) :

                login_user(user)
                flash('Log in Success!')

                next = request.args.get('next')
                if next == None or not next[0] =='/':
                    next = url_for('core.index')
                return redirect(next)
            elif user is not None and user.check_password(form.password.data) == False:
                error = 'Wrong Password'
            elif user is None:
                error = 'No such login Pls create one'
        return render_template('login.htm', form=form, error = error)
    else:
        return render_template('login_logout.htm')

@users.route('/account',methods = ['GET','POST'])
@login_required
def account():
    pic = current_user.profile_image
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data


        if form.picture.data is not None:
            id = current_user.id
            pic = add_profile_pic(form.picture.data,id)
            current_user.profile_image = pic

        flash('User Account Created')
        db.session.commit()
        redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email




    profile_image = url_for('static', filename= current_user.profile_image)
    return render_template('account.htm', profile_image=profile_image, form=form, pic = pic)

@users.route("/<username>")
def user_posts(username):
    maxi = 0
    mylist = []
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page = 5)

    for page_num in blog_posts.iter_pages(left_edge=1, right_edge = 1, left_current=1, right_current=2):
        mylist.append(page_num)

    maxi = max(mylist)
    return render_template('user_blog_post.htm', blog_posts = blog_posts, user = user,maxi = maxi)
