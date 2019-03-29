# coding:utf-8
from flask import render_template, request, redirect, url_for, flash, session
from admin import admin
from admin.forms.post import PostForm
from admin.forms.search import SearchForm
from admin.helper import content_file_handle, tags_handle, field_obj_set, to_dict
from common.extends import db
from common.models import Post, Classify, Style, Tag, Review

@admin.route('/post', methods=['GET', 'POST'])
def post():
    page = request.args.get('page',1,type=int)
    form = SearchForm(request.form)
    form.cid.choices = [(v.id, v.title) for v in db.session.query(Classify.id, Classify.title).all()]
    form.sid.choices = [(v.id, v.name) for v in Style.query.all()]
    if form.validate_on_submit():
        keywords = form.keywords.data
        posts = Post.query.filter_by(cid=form.cid.data, sid=form.sid.data).order_by(Post.id.desc())
        if not form.keywords.data:
            posts = posts.paginate(page=page, error_out=False)
        else:
            posts = posts.filter(Post.title.ilike('%'+keywords+'%')).paginate(page=page, error_out=False)
    else:
        posts = Post.query.filter(Post.sid>0).order_by(Post.id.desc()).paginate(page=page, error_out=False)
    args = dict(endpoint='admin.post')
    title = '文章管理'
    data = dict(title=title, pagination=posts, args=args, form=form)
    return render_template('admin/post.html', **data)

@admin.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def post_edit(id):
    post = Post.query.get(id)
    #转成字符串
    tags =  ','.join([tag.name for tag in post.tags])
    #转成表单默认数据
    data = to_dict(PostForm, post)
    data['tags'] = tags
    form = PostForm(data=data)
    form.cid.choices = [(v.id, v.title) for v in db.session.query(Classify.id, Classify.title).all()]
    form.sid.choices = [(v.id, v.name) for v in Style.query.all()]
    # 表单是否验证成功
    if form.validate_on_submit():
        form.content.data =content_file_handle(form.content.data, old_content=post.content)
        form.tags.data = tags_handle(form.tags.data,old=tags)
        post = field_obj_set(post,form.data)
        db.session.add(post)
        db.session.commit()
        db.session.close()
        flash('更新成功!', category='ok')
        return redirect(url_for('admin.post'))
    title = '更新文章'

    data = dict(title=title, form=form, tags=Tag.tags(), id=id)
    return render_template('admin/post.form.html', **data)

@admin.route('/post/add', methods=['GET', 'POST'])
def post_add():
    form = PostForm()
    form.cid.choices = [(v.id, v.title) for v in db.session.query(Classify.id, Classify.title).all()]
    form.sid.choices = [(v.id, v.name) for v in Style.query.all()]
    form.author.data = session.get('nikename')
    # 表单是否验证成功
    if form.validate_on_submit():
        form.tags.data = tags_handle(form.tags.data)
        form.content.data = content_file_handle(form.content.data)
        post = field_obj_set(Post(),form.data)
        db.session.add(post)
        db.session.commit()
        flash('添加成功!', category='ok')
        return redirect(url_for('admin.post_add'))
    title = '新建文章'
    data = dict(title=title, tags=Tag.tags(), form=form)
    return render_template('admin/post.form.html', **data)

@admin.route('/post/del')
def post_del():
    all = request.args.get('all',0)
    ids = [id for id in all.split(',') if id.isdigit()]
    if not ids:
        flash('数据不存在', category='err')
        return redirect(url_for('admin.post'))
    #查询出所有要删除的文章
    posts = db.session.query(Post).filter(Post.id.in_(ids)).all()
    for post in posts:
        # 删除文章中插入的图片
        content_file_handle('',old_content=post.content)
        # 删除无引用的标签
        tags_handle('',old=','.join([tag.name for tag in post.tags]))
        # 删除评论
        Review.query.filter(Review.pid == post.id).delete()
        db.session.delete(post)
    db.session.commit()
    db.session.close()
    flash('文章已删除', category='ok')
    return redirect(url_for('admin.post'))