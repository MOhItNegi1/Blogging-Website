
from flask import session
from models.post import Post
from extension import db
from flask import flash, redirect, url_for, abort

def list_posts(published):
    return Post.query.filter_by(is_published=published).all()

def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return post



def create_post(form):
    title = form.get('title', '').strip()
    body = form.get('body', '').strip()
    is_published = form.get('is_published') == 'on'

    # Get user_id from session
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to create a post.', 'error')
        return redirect(url_for('post.show_posts'))

    new_post = Post(title=title, body=body, is_published=is_published, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash('Post created successfully!', 'success')
    return redirect(url_for('post.show_posts'))

def update_post(post_id, form):
    post = get_post(post_id)
    title = form.get('title', '').strip()
    body = form.get('body', '').strip()
    is_published = 'is_published' in form

    if not title or not body:
        flash('Title and body are required.', 'error')
        return redirect(url_for('post.edit_post', post_id=post_id))

    post.title = title
    post.body = body
    post.is_published = is_published
    db.session.commit()
    flash('Post updated successfully!', 'success')
    return redirect(url_for('post.show_posts'))

def list_drafts():
    return list_posts(published=False)