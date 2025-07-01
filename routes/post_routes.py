from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.post_controller import list_posts, get_post, create_post, update_post, list_drafts
from extension import db
post = Blueprint('post', __name__, url_prefix='/posts')  


@post.route('/', methods=['GET'])
def show_posts():
    
    if session.get('role') == 'visitor' or not session.get('role'):
        posts = list_posts(published=True)
    else:
        #
        posts = list_posts(published=True)  
    return render_template('posts.html', posts=posts)


@post.route('/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    post_obj = get_post(post_id)
    if session.get('role') == 'visitor' and not post_obj.is_published:
        flash('You do not have permission to view this post.', 'error')
        return redirect(url_for('post.show_posts'))
    return render_template('post_detail.html', post=post_obj)

@post.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        return create_post(request.form)
    return render_template('post_form.html')

@post.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        return update_post(post_id, request.form)
    post_obj = get_post(post_id)
    return render_template('post_form.html', post=post_obj)

@post.route('/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if session.get('role') == 'visitor':
        flash('Visitors are not allowed to delete posts.', 'error')
        return redirect(url_for('post.show_posts'))
    post_obj = get_post(post_id)
    db.session.delete(post_obj)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('post.show_posts'))