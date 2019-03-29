# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TagForm(FlaskForm):

    name = StringField(
        label='名称',
        description='名称',
        validators=[
            DataRequired('标签名称必填')
        ],
        render_kw={
            'class':'form-control',
            'placeholder': '标签名称必填',
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary btn-lg',
        }
    )