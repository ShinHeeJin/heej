from flask import current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from app.exceptions import ValidationError
from . import db, login_manager


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop("_with_deleted", False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(
            db.class_mapper(self._mapper_zero().class_),
            session=db.session(),
            _with_deleted=True,
        )

    def _get(self, *args, **kwargs):
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None

class PostLike(db.Model):
    __tablename__ = "USER_POST_LIKE"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("USER.id"), primary_key=True)
    post_id = db.Column(db.BigInteger, db.ForeignKey("POST.id"), primary_key=True)
    user = db.relationship("User", back_populates="like_posts")
    post = db.relationship("Post", back_populates="like_users")

class User(UserMixin, db.Model):
    __tablename__ = "USER"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(64), unique=False)
    confirmed = db.Column(db.Boolean, default=False)

    abount_me = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Enum("M", "F"), nullable=True)
    birth = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    job = db.Column(db.String(255), nullable=True)

    last_seen = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)
    posts = db.relationship("Post", backref="user", lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    like_posts = db.relationship("PostLike", back_populates="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"reset": self.id}).decode("utf-8")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        user = User.query.get(data.get("reset"))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    def is_liked_post(self, post):
        return True if self.like_posts.filter_by(post=post).first() else False

    def like_post(self, post):
        if not self.is_liked_post(post):
            new_post_like = PostLike(user=self, post=post)
            db.session.add(new_post_like)

    def unlike_post(self, post):
        if self.is_liked_post(post):
            self.like_posts.filter_by(post=post).delete()

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = "POST"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("USER.id"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")
    like_users = db.relationship("PostLike", back_populates="post", lazy="dynamic")
    query_class = QueryWithSoftDelete

    # def to_json(self):
    #     json_post = {
    #         "url": url_for("api.get_post", id=self.id),
    #         "content": self.content,
    #         "created_at": self.created_at,
    #         "author_url": url_for("api.get_user", id=self.author_id),
    #         "comments_url": url_for("api.get_post_comments", id=self.id),
    #         "comment_count": self.comments.count(),
    #     }
    #     return json_post

    # @staticmethod
    # def from_json(json_post):
    #     content = json_post.get("content")
    #     if content is None or content == "":
    #         raise ValidationError("post does not have a content")
    #     return Post(content=content)


class Comment(db.Model):
    __tablename__ = "COMMENT"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    disabled = db.Column(db.Boolean)
    user_id = db.Column(db.BigInteger, db.ForeignKey("USER.id"))
    post_id = db.Column(db.BigInteger, db.ForeignKey("POST.id"))

    # def to_json(self):
    #     json_comment = {
    #         "url": url_for("api.get_comment", id=self.id),
    #         "post_url": url_for("api.get_post", id=self.post_id),
    #         "content": self.content,
    #         "created_at": self.created_at,
    #         "author_url": url_for("api.get_user", id=self.author_id),
    #     }
    #     return json_comment

    # @staticmethod
    # def from_json(json_comment):
    #     content = json_comment.get("content")
    #     if content is None or content == "":
    #         raise ValidationError("comment does not have a content")
    #     return Comment(content=content)
