from . import auth
from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from .. import db
from ..models import User
from ..email import send_email
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user

# 로그인
@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("메일 혹은 비밀번호가 유효하지 않습니다.")
    return render_template("auth/login.html", form=form)


# 회원가입
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form)
        user = User(email=form.email.data.lower(), name=form.name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, "인증메일 발송", "auth/email/confirm", user=user, token=token)
        flash("인증메일이 발송되었습니다. 메일을 확인해주세요")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


# 메일 인증
@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("메일 인증이 완료되었습니다!")
    else:
        flash("인증링크가 유효하지 않거나 인증이 만료되었습니다.")
    return redirect(url_for("main.index"))


# 로그아웃
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# 비밀번호 변경
@auth.route("/reset", methods=["GET", "POST"])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, "비밀번호 재설정", "auth/email/reset_password", user=user, token=token)
        flash("비밀번호 재설정을 위한 안내메일이 발송되었습니다.")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


# 비밀번호 변경 2
@auth.route("/reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("비밀번호가 변경되었습니다.")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("main.index"))
    return render_template("auth/change_password.html", form=form)