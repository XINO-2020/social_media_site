from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    picture = FileField('Any Picture ', validators=[FileAllowed(['jpg', 'png'])])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')
