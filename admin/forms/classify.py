# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired

class ClassifyForm(FlaskForm):

    title = StringField(
        label='名称',
        description='名称',
        validators=[
            DataRequired('分类名称必填')
        ],
        render_kw={
            'class':'form-control',
            'placeholder': '分类名称必填',
        }
    )

    sort = IntegerField(
        label='排序',
        description='排序',
        default=100,
        validators=[
            DataRequired('必须是一个整数'),
        ],
        render_kw={
            'class':'form-control',
            'placeholder': '分类先后排序',
        }
    )

    asn = BooleanField('禁止显示在导航栏',default=0)

    cover = FileField(
        label='封面',
        description='封面',
        render_kw={
            'class':'form-control',
            'placeholder': '分类封面',
            'accept':'.gif,.jpg,.jpeg,.png'
        }
    )

    keywords = StringField(
        label='SEO关键词',
        description='SEO关键词',
        render_kw={
            'class': 'form-control',
            'placeholder': 'SEO关键词',
        }
    )

    desc = TextAreaField(
        label='SEO描述',
        description='SEO描述',
        render_kw={
            'class': 'form-control',
            'placeholder': 'SEO描述',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary btn-lg',
        }
    )