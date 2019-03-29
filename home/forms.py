# coding:utf-8
from urllib.request import Request, urlopen
from flask import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from common.configs import VAPTCHA_ID, VAPTCHA_SECRET_KEY

class VaptchaForm(FlaskForm):
    api_url = 'http://api.vaptcha.com/v2/validate'
    api_id  = VAPTCHA_ID,
    api_key = VAPTCHA_SECRET_KEY,

    vaptcha_token = StringField()

    def validate_vaptcha_token(self,field):
        uri = 'id={}&secretkey={}&token={}'.format(VAPTCHA_ID,VAPTCHA_SECRET_KEY,field.data)
        uri = bytes(uri,encoding='utf-8')

        request3 = Request(self.api_url, data=uri)
        response = urlopen(request3)
        html = response.read().decode('utf-8')
        jsond = json.loads(html)

        if jsond.get('success') != 1: raise ValidationError('请先进行人机验证')


class LoginForm(VaptchaForm):

    username = StringField(
        label='帐户',
        description='帐户',
        validators=[
            DataRequired('帐户不能为空!')
        ],
        render_kw={
            'class':'layui-input',
            'placeholder':'请输入帐户',
            'required':'required',
            'lay-verify':'required',
            'autocomplete':'off',
        }
    )

    password = PasswordField(
        label='密码',
        description='密码',
        validators=[
            DataRequired('密码不能为空!')
        ],
        render_kw={
            'class':'layui-input',
            'placeholder':'请输入密码',
            'required':'required',
            'lay-verify':'required',
            'autocomplete':'off',
        }
    )

    submit = SubmitField(
        '立即登录',
        render_kw={
            'class': 'layui-btn',
            'lay-filter':'*',
            'lay-submit':None
        }
    )

class ReviewForm(VaptchaForm):
    email = StringField(
        label='邮箱',
        description='邮箱',
        validators=[
            DataRequired('邮箱必填!'),
            Length(max=50, message='邮箱长度不能超过50个字符'),
            Email('邮箱格式错误'),

        ],
        render_kw={
            'lay-verify':'email',
            'lay-vertype':'tips',
            'placeholder':'请输入邮箱',
            'autocomplete':'off',
            'class':'layui-input'
        }
    )

    name = StringField(
        label='昵称',
        description='昵称',
        validators=[
            Length(max=22, message='昵称长度不能超过22个字符'),
            DataRequired('昵称必填'),
        ],
        render_kw={
            'lay-verify':'nickname',
            'lay-vertype':'tips',
            'placeholder':'请输入昵称',
            'autocomplete':'off',
            'class':'layui-input'
        }
    )

    comment = TextAreaField(
        label='评论内容',
        description='评论内容',
        validators=[
            DataRequired('评论内容必填!'),
            Length(max=250,message='评论内容最大长度250字符')
        ],
        render_kw={
            'lay-verify': 'comment',
            'lay-vertype': 'msg',
            'placeholder': '请输入内容',
            'class':'layui-textarea fly-editor',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'layui-btn',
            'lay-filter':'*',
            'lay-submit':None
        }
    )