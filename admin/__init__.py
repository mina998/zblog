# coding:utf-8
from flask import Blueprint, session, redirect, url_for

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def verify_login():
    if session.get('login') != 1:
        return redirect(url_for('home.login'))


@admin.context_processor
def get_breadcrumb():
    data = [
        dict(id=2, pid=0, url='admin.classify', name='分类管理'),
        dict(id=3, pid=2, url='admin.classify_add', name='添加分类'),
        dict(id=4, pid=2, url='admin.classify_edit', name='修改分类'),
        dict(id=5, pid=0, url='admin.post', name='文章管理'),
        dict(id=6, pid=5, url='admin.post_add', name='添加文章'),
        dict(id=7, pid=5, url='admin.post_edit', name='修改文章'),
        dict(id=8, pid=0, url='admin.tag', name='标签管理'),
        dict(id=9, pid=8, url='admin.tag_edit', name='编辑标签'),
        dict(id=1, pid=0, url='admin.review', name='评论管理'),
        dict(id=10, pid=0, url='admin.site', name='站点管理'),
        dict(id=11, pid=0, url='admin.user', name='个人资料'),
        dict(id=12, pid=0, url='admin.login_set', name='修改密码'),
    ]
    bd = []
    def breadcrumb2(id=None):
        for item in data:
            if item.get('id') == id:
                bd.insert(0,item)
                breadcrumb2(id=item.get('pid'))
        return bd

    return dict(breadcrumb=breadcrumb2)

from admin import index
from admin import post
from admin import classify
from admin import tag
from admin import review
