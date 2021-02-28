from . import user
from flask import render_template, redirect, url_for, request, current_app, flash, jsonify
from flask_login import login_required, current_user
from ..models import User, Post, Comment
from .forms import PostForm, EditProfileForm
from ..main.forms import CommentForm
from .. import db


@user.route("/<int:user_id>")
def user_page(user_id):
    form = CommentForm()
    user = User.query.get_or_404(user_id)
    page = request.args.get("page", 1, type=int)
    post_id = request.args.get("postId", None)
    post = Post.query.get(post_id)
    pagination = (
        user.posts.filter_by(deleted=False)
        .order_by(Post.created_at.desc())
        .paginate(page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False)
    )
    posts = pagination.items
    return render_template(
        "user.html", user=user, posts=posts, pagination=pagination, form=form, post=post
    )


@user.route("/post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        post = Post(content=form.content.data, user=user)
        db.session.add(post)
        db.session.commit()
        flash("게시글이 작성되었습니다.")
        return redirect(url_for("user.user_page", user_id=current_user.id))

    return render_template("user/post.html", form=form)


@user.route("/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user._get_current_object())
    if form.validate_on_submit():
        user = current_user._get_current_object()
        form.populate_obj(user)
        db.session.commit()
        flash("프로필이 수정 되었습니다.")
        return redirect(url_for("user.user_page", user_id=current_user.id))
    return render_template("user/profile.html", form=form)


@user.route("/post/<int:post_id>/<string:end_point>/<int:page>", methods=["POST"])
@login_required
def add_comment(post_id, end_point, page=1):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comment = Comment(
        content=form.content.data.strip(), user=current_user._get_current_object()
    )
    post.comments.append(comment)
    db.session.commit()
    flash("댓글이 추가되었습니다.")
    return redirect(
        url_for(end_point, user_id=comment.post.user.id, page=page, postId=post.id)
    )


@user.route("/comment/<int:comment_id>/<string:end_point>/<int:page>", methods=["POST"])
@login_required
def edit_comment(comment_id, end_point, page=1):
    form = CommentForm()
    comment = Comment.query.get(comment_id)
    post_id = comment.post.id
    comment.content = form.content.data.strip()
    db.session.commit()
    flash("댓글이 수정되었습니다.")
    return redirect(
        url_for(end_point, user_id=comment.post.user.id, page=page, postId=post_id)
    )


@user.route(
    "/comment/delete/<int:comment_id>/<string:end_point>/<int:page>", methods=["POST"]
)
@login_required
def delete_comment(comment_id, end_point, page=1):
    comment = Comment.query.get(comment_id)
    post_id = comment.post.id
    comment.deleted = True
    db.session.commit()
    return redirect(
        url_for(end_point, user_id=comment.post.user.id, page=page, postId=post_id)
    )

@user.route("/post/<int:post_id>/like", methods=['POST', 'FETCH'])
def update_post_like_status(post_id):
    post = Post.query.get(post_id)
    
    print(current_user)

    if request.method == 'POST':
        if current_user.is_liked_post(post):
            current_user.unlike_post(post)
        else:
            current_user.like_post(post)
        db.session.commit()
        return jsonify({'isLiked':current_user.is_liked_post(post)})
    
    else:
        print('update_post_like_status / fetch')
        return jsonify({'count':post.like_users.count()})
