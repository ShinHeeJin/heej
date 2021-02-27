from . import main
from flask import render_template, request, current_app
from ..models import Post

@main.route("/", methods=["GET", "POST"])
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    return render_template("index.html", posts=posts, pagination=pagination)
