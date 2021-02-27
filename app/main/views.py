from . import main
from flask import render_template, request, current_app
from ..models import Post
from .forms import CommentForm

@main.route("/", methods=["GET"])
def index():
    form = CommentForm()
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    return render_template("index.html", posts=posts, pagination=pagination, form=form)
