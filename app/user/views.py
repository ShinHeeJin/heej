from . import user
from flask import render_template, redirect, url_for, request, current_app, make_response
from flask_login import login_required, current_user
from ..models import User, Post
from .forms import PostForm, EditProfileForm
from .. import db


@user.route("/user/<int:user_id>")
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get("page", 1, type=int)
    pagination = user.posts.order_by(Post.created_at.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    return render_template("user.html", user=user, posts=posts, pagination=pagination)


@user.route("/user/post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        user = current_user._get_current_object()
        post = Post(content=form.content.data, user=user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("user.user_page", user_id=current_user.id))

    return render_template("user/post.html", form=form)

@user.route("/user", methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user._get_current_object())
    if form.validate_on_submit():
        user = current_user._get_current_object()
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("user.user_page", user_id=current_user.id))
    return render_template("user/profile.html", form=form)
