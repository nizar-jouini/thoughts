from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User

@app.route('/thoughts')
def thoughts():
    logged_user = User.get_by_id({'id' : session['user_id']})
    posts = Post.get_all()
    return render_template('dashboard.html', logged_user = logged_user, posts = posts)

@app.route('/posts/new', methods=['POST'])
def create():
    if not Post.validation(request.form):
        return redirect('/thoughts')
    Post.create(request.form)
    return redirect('/thoughts')

@app.route('/users/<int:id>')
def show(id):
    logged_user = User.get_by_id({'id' : session['user_id']})
    post = Post.get_by_id({'id': id})
    return render_template('show_post.html', post = post, logged_user = logged_user)

@app.route('/posts/delete/<int:id>')
def delete(id):
    result = Post.delete({'id': id})
    return redirect('/thoughts')

@app.route('/posts/unlike/<int:post_id>')
def unlike(post_id):
    Post.delete_like({'post_id' : post_id})
    return redirect('/thoughts')

@app.route('/posts/like/<int:post_id>')
def like(post_id):
    Post.add_like({'user_id' : session['user_id'], 'post_id' : post_id})
    return redirect('/thoughts')
