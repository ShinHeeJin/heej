from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    content = TextAreaField('게시글 작성', validators=[DataRequired("내용을 입력해주세요")], render_kw={'rows': 20})
    submit = SubmitField("등록", render_kw={'class':'btn btn-secondary'})