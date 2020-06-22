# core/views.py
from blogs.models import BlogPost
from flask import Blueprint,render_template,request, url_for
from flask_login import current_user

core = Blueprint('core',__name__)

@core.route('/')
def index():
    maxi = 0
    n = 0
    mylist = [1]
    page = request.args.get('page',1,type = int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    for page_num in blog_posts.iter_pages(left_edge=1, right_edge = 1, left_current=1, right_current=2):
        mylist.append(page_num)
        n+=1

    maxi = max(mylist)
    return render_template('index.htm',blog_posts=blog_posts, maxi  =maxi, n=n)

@core.route('/info')
def info():
    return render_template('info.htm')
