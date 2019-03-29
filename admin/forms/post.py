# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    cid = SelectField(
        label='所属类别',
        description='所属类别',
        coerce=int,
        choices='',
        validators=[
            DataRequired('请选择类别!')
        ],
        render_kw={
            'class':'form-control',
            'placeholder':'请选择类别!',
        }
    )

    title = StringField(
        label='标题',
        description='标题',
        validators=[
            DataRequired('标题必填!'),
            Length(max=40,message='标题最大长度不能超过40个字符')
        ],
        render_kw={
            'class':'form-control',
        }
    )

    content = TextAreaField(
        label='正文',
        description='正文',
        validators=[
            DataRequired('正文必填!')
        ],
        render_kw={
            'class':'form-control wangEditor hidden',
        }
    )

    tags = StringField(
        label='标签',
        description='标签',
        render_kw={
            'class':'form-control',
            'placeholder':'标签用英文,分隔',
        }
    )

    summary = TextAreaField(
        label='摘要',
        description='摘要',
        render_kw={
            'class':'form-control',
            'placeholder':'文章摘要',
            'style': 'min-height:90px'
        }
    )

    keywords = StringField(
        label='SEO关键词',
        description='SEO关键词',
        render_kw={
            'class':'form-control',
            'placeholder':'SEO关键词用,分隔',
        }
    )

    desc = TextAreaField(
        label='SEO描述',
        description='SEO描述',
        render_kw={
            'class':'form-control',
            'placeholder':'SEO描述',
            'style': 'min-height:90px'
        }
    )

    sid = SelectField(
        label='状态',
        description='状态',
        coerce=int,
        choices='',
        validators=[
            DataRequired('请选择状态')
        ],
        render_kw={
            'class':'form-control',
            'placeholder':'请选择状态',
        }
    )

    passwd = StringField(
        label='查看密码',
        description='查看密码',
        render_kw={
            'class':'form-control',
            'placeholder':'请输入查看密码',
        }
    )

    author = StringField(
        label='作者',
        description='作者',
        render_kw={
            'class':'form-control',
            'placeholder':'作者',
        }
    )

    is_review = BooleanField('禁止评论',default=0)

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary btn-block btn-lg',
        }

    )