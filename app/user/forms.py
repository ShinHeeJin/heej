from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email


class PostForm(FlaskForm):
    content = TextAreaField(
        "게시글 작성", validators=[DataRequired("내용을 입력해주세요")], render_kw={"rows": 20}
    )
    submit = SubmitField("등록", render_kw={"class": "btn btn-secondary"})


class EditProfileForm(FlaskForm):
    email = StringField(
        "이메일",
        validators=[DataRequired(), Length(1, 64), Email()],
        render_kw={"readonly": True},
    )
    name = StringField("이름", validators=[DataRequired(), Length(1, 64)])
    abount_me = TextAreaField("상태메세지")
    gender = SelectField("성별", choices=[("F", "여자"), ("M", "남자")])
    birth = DateField("생년월일")
    location = StringField("지역")
    job = StringField("직업")
    submit = SubmitField("수정", render_kw={"class": "btn btn-secondary"})