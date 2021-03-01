import os
from app import create_app, db
from app.models import *
from flask import render_template, request, jsonify

app = create_app(os.environ.get("FLASK_CONFIG") or "default")


@app.shell_context_processor
def make_shell_context():
    users = User.query.all()
    if not users:
        new_user = User(name="test", email="test@example.com", password="test1234!")
        db.session.add(new_user)
        db.session.commit()
        user = new_user
    else:
        user = users[0]

    posts = Post.query.all()
    if not posts:
        new_post = Post(content="test")
        db.session.add(new_post)
        db.session.commit()
        post = new_post
    else:
        post = posts[0]

    comment = None
    if post.comments.all():
        comment = post.comments.all()[0]
    else:
        new_comment = Comment(content="test", user=user, post=post)
        db.session.add(new_comment)
        db.session.commit()
        comment = new_comment

    return dict(
        db=db,
        user=user,
        post=post,
        comment=comment,
        User=User,
        Post=Post,
        Comment=Comment,
        PostLike=PostLike,
        CommentLike=CommentLike,
    )


@app.errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "forbidden"})
        response.status_code = 403
        return response
    return render_template("error/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "internal server error"})
        response.status_code = 500
        return response
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)