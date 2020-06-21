# core/views.py
from blogs.models import BlogPost
from flask import Blueprint,render_template,request, url_for
from flask_login import current_user

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type = int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('index.htm',blog_posts=blog_posts)

@core.route('/info')
def info():
    return render_template('info.htm')
