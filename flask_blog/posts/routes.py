from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm
from flask_blog.posts.utils import save_picture

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post_db = Post(title=form.title.data, excerpt=form.excerpt.data, content=form.content.data, author=current_user, image_file=picture_file)
        else:
            post_db = Post(title=form.title.data, excerpt=form.excerpt.data, content=form.content.data, author=current_user)
        db.session.add(post_db)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            print(picture_file)
            print(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.excerpt = form.excerpt.data
        post.content = form.content.data
        db.session.commit()
        flash('You post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    
    form.title.data = post.title
    form.excerpt.data = post.excerpt
    form.content.data = post.content

    return render_template('create_post.html', title='Update ' + post.title, post=post, form=form, legend='Update Post')

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('You post has been deleted!', 'success')
    return redirect(url_for('main.home'))