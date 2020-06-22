#blogpost/views
from flask import abort, render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from blogs import db
from blogs.models import BlogPost
from blogs.blogpost.forms import BlogPostForm
from blogs.blogpost.picture_handler import add_blog_pic

blogpost  =Blueprint('blogpost', __name__)

###crud
#c
@blogpost.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                                text=form.text.data,
                                user_id=current_user.id)
        if form.picture.data is not None:
            id = current_user.id
            pic = add_blog_pic(form.picture.data,id)
            blog_post.blog_image = pic
            db.session.commit()
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))
    return render_template('create_post.htm', form = form)

#r
@blogpost.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    blog_image = url_for('static', filename= blog_post.blog_image)
    return render_template('blog_post.htm', title = blog_post.title,
                            date = blog_post.date, post = blog_post, text = blog_post.text, blog_image = blog_image)
#u
@blogpost.route('/<int:blog_post_id>/update',methods = ['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blogpost.blog_post', blog_post_id = blog_post_id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.htm', title = 'Updating', form= form)

#d
@blogpost.route('/<int:blog_post_id>/delete',methods = ['GET','POST'])
@login_required
def delete(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))
