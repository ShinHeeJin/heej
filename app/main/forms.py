from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = TextField('댓글', validators=[DataRequired("내용을 입력해주세요")], render_kw={'class':'form-control'})
    submit = SubmitField("등록", render_kw={'class':'btn btn-secondary'})