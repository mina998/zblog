# coding:utf-8
from platform import platform
from sqlite3 import sqlite_version
from sys import version

from admin import admin
from flask import render_template, request, jsonify, flash, redirect, url_for, current_app as app, session
from admin.forms.site import SiteForm
from admin.forms.user import UserForm, LoginForm
from admin.helper import file_move_to, file_delete
from common.extends import db
from common.models import Site, Post, Classify, Review, Tag
from common.uploads import Uploads
from common.util import site_to_dict


@admin.route('/')
def index():
    pvs = db.session.query(db.func.sum(Post.view).label('pvs')).one()
    data = dict(
        title='仪表盘',
        posts = Post.query.count(),
        classifys = Classify.query.count(),
        reviews = Review.query.count(),
        tags = Tag.query.count(),
        pvs = pvs.pvs,
        name = 'ZBlog',
        framework = 'Flask 1.0.2',
        author = 'Soros',
        contact = 'QQ519999189',
        discuss = '<a target="_blank" href="http://shang.qq.com/wpa/qunwpa?idkey=65deab2f8ea1e9d2445c3262d133da48fe9de53bd90a3146c3f7bb6fb9d63ead"><img border="0" src="http://pub.idqqimg.com/wpa/images/group.png" alt="zui-admin后台模板交流" title="zui-admin后台模板交流"></a>',
        os = platform(),
        python2 = version,
        data_driven = app.config.get('SQLALCHEMY_DATABASE_URI').split(':')[0] +'.'+ sqlite_version,
        up_file_max=app.config.get('MAX_CONTENT_LENGTH') / 1024 / 1024
    )

    db.create_all()
    return render_template('admin/index.html', **data)

@admin.route('/logout')
def logout():
    session.pop('login',None)
    session.pop('nikename',None)
    return redirect(url_for('admin.index'))

@admin.route('/image/up', methods=['POST'])
def image_up():
    # 上传图片
    files = request.files
    files = [files.get(i) for i in files]
    paths = Uploads(files).save()

    datas = paths.data if isinstance(paths.data,list) else [paths.data]

    data = {
        "errno": paths.err,
        "data" : datas
    }
    return jsonify(data)


@admin.route('/site', methods=['GET','POST'])
def site():
    default = {}
    site = Site.query.all()
    for item in site:
        if hasattr(SiteForm,item.name): default[item.name] = item.value
    form = SiteForm(data=default)
    if form.validate_on_submit():
        for key,value in form.data.items(): Site.query.filter_by(name=key).update({'value':value})
        db.session.commit()
        flash('修改成功', category='ok')

    title = '站点管理'
    data = dict(title=title, form=form)
    return render_template('admin/config.html', **data)

@admin.route('/user', methods=['GET','POST'])
def user():
    default = site_to_dict(Site.query.filter_by(group='user').all())
    avatar = default['avatar']
    form = UserForm(data=default)
    if form.validate_on_submit():
        if not form.avatar.data: form.avatar.data = avatar
        else:
            path = Uploads(form.avatar.data).save()
            if path.err ==1:
                flash('不充许上传:%s'%path.data, category='err')
                return redirect(url_for('admin.classify_add'))
            file_delete(avatar)
            avatar = form.avatar.data = file_move_to(path.data)
        for key,value in form.data.items():
            Site.query.filter_by(name=key).update({'value':value})

        db.session.commit()
        flash('修改成功', category='ok')
    db.session.close()
    title = '个人资料'
    data = dict(title=title, form=form)
    return render_template('admin/user.html', **data, avatar=avatar)


@admin.route('/login/set', methods=['GET','POST'])
def login_set():
    user = Site.query.filter(Site.name.in_(['username','password'])).all()
    form = LoginForm(data=site_to_dict(user))
    if form.validate_on_submit():
        for key,value in form.data.items():
            Site.query.filter_by(name=key).update({'value':value})
        db.session.commit()
        flash('修改成功', category='ok')
    db.session.close()
    title = '修改密码'
    data = dict(title=title, form=form)
    return render_template('admin/login.set.html', **data)