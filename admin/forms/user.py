# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):

    nikename = StringField(
        label='昵称',
        description='昵称',
        render_kw={
            'class':'form-control',
            'placeholder': '昵称',
        }
    )
    avatar = FileField(
        label='头像',
        description='头像',
        render_kw={
            'class':'form-control',
            'placeholder': '头像',
            'accept':'.gif,.jpg,.jpeg,.png'
        }
    )
    email = StringField(
        label='邮箱',
        description='邮箱',
        render_kw={
            'class':'form-control',
            'placeholder': '邮箱',
        }
    )
    profile = TextAreaField(
        label='简介',
        description='简介',
        render_kw={
            'class':'form-control',
            'placeholder': '简介',
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary btn-lg',
        }
    )

class LoginForm(FlaskForm):

    username = StringField(
        label='用户名',
        description='用户名',
        validators=[
            DataRequired('用户名必填')
        ],
        render_kw={
            'class':'form-control',
            'placeholder': '用户名',
        }
    )
    password = StringField(
        label='密码',
        description='密码',
        validators=[
            DataRequired('密码必填')
        ],
        render_kw={
            'class':'form-control',
            'placeholder': '密码',
        }
    )

    submit = SubmitField(
        '修改',
        render_kw={
            'class': 'btn btn-primary btn-lg',
        }
    )