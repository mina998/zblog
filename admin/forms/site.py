# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class SiteForm(FlaskForm):

    title = StringField(
        label='网站名称',
        description='网站名称',
        validators=[
            DataRequired('网站名称不能为空!')
        ],
        render_kw={
            'class':'form-control',
            'autocomplete':'off',
            'placeholder': '网站名称必填',
        }
    )
    keywords = StringField(
        label='SEO关键词',
        description='SEO关键词',
        render_kw={
            'class':'form-control',
            'placeholder': 'SEO关键词',
            'placeholder': '每个关键词之间用英文,号隔开. 例: ZBlog,Z博客,Python博客,博客程序',
        }
    )
    desc = TextAreaField(
        label='SEO描述',
        description='SEO描述',
        render_kw={
            'class':'form-control',
            'placeholder': '简短描述站点信息,200字以内. 将显示在搜索引擎中',
        }
    )
    switch = RadioField(
        label = '站点开关',
        choices=[
            ('1', u'开启'),
            ('2', u'关闭')
        ],
        validators=[
            DataRequired('站点开关必须选择!')
        ]
    )
    mark = TextAreaField(
        label='关站说明',
        description='关站说明',
        render_kw={
            'class':'form-control',
            'placeholder': '关站说明',
        }
    )

    upfiletype = StringField(
        label='允许上传文件类型',
        description='允许上传文件类型',
        render_kw={
            'class':'form-control',
            'placeholder': '用#符号开,例: jpg#png#gif',
        }
    )

    copyright = TextAreaField(
        label='版权信息',
        description='版权信息',
        render_kw={
            'class':'form-control',
            'placeholder': '版权信息',
        }
    )

    tongji = TextAreaField(
        label='统计代码',
        description='统计代码',
        render_kw={
            'class':'form-control',
            'placeholder': 'JS追踪代码',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary btn-lg',
        }
    )