from datetime import datetime
from blogs import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    fname = db.Column(db.String(64))
    profile_image = db.Column(db.String(64), nullable = False, default = 'Site_icon.png')
    email = db.Column(db.String(64),unique = True,index = True)
    username = db.Column(db.String(64),unique = True,index = True)
    password_hash = db.Column(db.String(128))
    reply = db.relationship('Reply' , backref = 'user_reply', lazy = 'dynamic')

    posts = db.relationship('BlogPost', backref = 'author' ,lazy = True)

    def __init__(self, fname, email, username, password):
        self.email = email
        self.fname =fname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

class BlogPost(db.Model):

    __tablename__ = 'blogs'
    users = db.relationship(User)
    reply = db.relationship('Reply' , backref = 'blog_reply' , lazy = 'dynamic')
    blog_image = db.Column(db.String(64), nullable = False, default = 'None.png')
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable = False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable = False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post id {self,id} -- Date: {self.date} --- {self.title}"
class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer,primary_key = True)
    reply = db.Column(db.String)
    time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user = db.relationship(User)
    blog = db.relationship(BlogPost)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))

    def __init__(self,reply,user_id,blog_id):
        self.reply = reply
        self.user_id = user_id
        self.blog_id = blog_id
