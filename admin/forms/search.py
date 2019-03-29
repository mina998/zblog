# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
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
    keywords = StringField(
        label='关键词',
        description='关键词',
        render_kw={
            'class':'form-control',
            'placeholder':'关键词',
        }
    )
    submit = SubmitField(
        '查询',
        render_kw={
            'class': 'btn',
        }
    )
