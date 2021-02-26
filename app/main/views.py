from . import main
from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from ..models import Post
from .. import db

@main.route("/test")
def test():
    return render_template("test.html")


@main.route("/", methods=["GET", "POST"])
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    return render_template("index.html", posts=posts, pagination=pagination)
