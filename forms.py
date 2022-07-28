from flask_wtf import FlaskForm
from wtforms import SubmitField, MultipleFileField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    photo = MultipleFileField(render_kw={'multiple': True}, validators=[DataRequired()])
    submit = SubmitField("Submit")
