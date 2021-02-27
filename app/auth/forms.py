from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField(
        "이메일",
        validators=[
            DataRequired("이메일을 입력해 주세요"),
            Length(1, 64),
            Email("이메일 형식을 확인해 주세요"),
        ],
    )
    name = StringField(
        "이름", validators=[DataRequired("이름을 입력해 주세요"), Length(1, 64)]
    )
    password = PasswordField(
        "비밀번호",
        validators=[
            DataRequired(),
            EqualTo("password2", message="비밀번호가 일치하지 않습니다."),
        ],
    )
    password2 = PasswordField("비밀번호 확인", validators=[DataRequired()])
    submit = SubmitField("회원가입")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("이메일이 이미 존재합니다.")


class LoginForm(FlaskForm):
    email = StringField("이메일", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    remember_me = BooleanField("이메일 저장")
    submit = SubmitField("로그인")


class PasswordFindRequestForm(FlaskForm):
    email = StringField(
        "이메일", validators=[DataRequired(), Length(1, 64), Email("이메일 형식을 확인해주세요")]
    )
    submit = SubmitField("이메일 전송")

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("이메일이 존재하지 않습니다.")


class PasswordFindForm(FlaskForm):
    password = PasswordField(
        "새로운 비밀번호",
        validators=[DataRequired(), EqualTo("password2", message="비밀번호가 일치하지 않습니다.")],
    )
    password2 = PasswordField("비밀번호 확인", validators=[DataRequired()])
    submit = SubmitField("변경하기")

class PasswordResetRequestForm(FlaskForm):
    origin_password = PasswordField("기존 비밀번호", validators=[DataRequired("정보를 입력해주세요")])
    new_password = PasswordField("새로운 비밀번호", validators=[DataRequired("정보를 입력해주세요"), EqualTo("confirm_password")])
    confirm_password = PasswordField("새로운 비밀번호", validators=[DataRequired("정보를 입력해주세요")])
    submit = SubmitField("변경")

    def __init__(self, user, *args, **kwargs):
        super(PasswordResetRequestForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_origin_password(self, field):
        if not self.user.verify_password(field.data):
            raise ValidationError("비밀번호가 일치하지 않습니다.")

    def validate_new_password(self, field):
        if self.user.verify_password(field.data):
            raise ValidationError("기존 비밀번호와 동일합니다.")