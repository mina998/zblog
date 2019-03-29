# coding:utf-8
from flask import render_template, url_for, flash, redirect, request, jsonify
from admin.helper import file_move_to, field_obj_set, to_dict, file_delete
from admin.forms.classify import ClassifyForm
from common.uploads import Uploads
from common.extends import db
from common.models import Classify, Post
from admin import admin


@admin.route('/classify')
def classify():
    title = '分类管理'
    subQuery = db.session.query(db.func.count(Post.id)).filter(Post.cid == Classify.id).correlate(Classify).label('pnum')
    classify = db.session.query(Classify.id, Classify.sort, Classify.title, Classify.asn, subQuery).all()
    data = dict(title=title, classify=classify)
    return render_template('admin/classify.html', **data)

@admin.route('/classify/del', methods=['GET', 'POST'])
def classify_del():
    ids = [request.args.get('id')]
    if request.method == 'POST': ids = request.form.getlist('id')
    for id in ids:
        classify = Classify.query.get(id)
        if classify.posts:
            flash('请先删除该分类下文章:[%s]' % classify.title, category='err')
        else:
            file_delete(classify.cover)
            db.session.delete(classify)
            db.session.commit()
            flash('删除完成:[%s]' % classify.title, category='ok')
    return redirect(url_for('admin.classify'))

@admin.route('/classify/add', methods=['GET', 'POST'])
def classify_add():
    form = ClassifyForm()
    # 表单是否验证成功
    if form.validate_on_submit():
        # 获取上传图片地址
        if not form.cover.data: form.cover.data = ''
        else:
            path = Uploads(form.cover.data).save()
            if path.err ==1:
                flash('不允许上传:%s'%path.data, category='err')
                return redirect(url_for('admin.classify_add'))
            form.cover.data = file_move_to(path.data)
        classify = field_obj_set(Classify(),form.data)
        db.session.add(classify)
        db.session.commit()
        flash('添加成功!', category='ok')
        return redirect(url_for('admin.classify_add'))
    title = '添加分类'
    data = dict(title=title, form=form)
    return render_template('admin/classify.form.html', **data)

@admin.route('/classify/edit/<int:id>', methods=['GET', 'POST'])
def classify_edit(id):

    classify = Classify.query.get_or_404(id)
    cover = classify.cover
    # 删除封面
    if request.args.get('cover') == 'del':
        classify.cover = ''
        db.session.add(classify)
        db.session.commit()
        file_delete(cover)
        return jsonify(dict(err=0))

    form = ClassifyForm(data=to_dict(ClassifyForm,classify))
    # 表单是否验证成功
    if form.validate_on_submit() and request.method=='POST':
        # 获取上传图片地址
        if not form.cover.data: form.cover.data = cover
        else:
            path = Uploads(request.files.get('cover')).save()
            if path.err ==1:
                flash('不允许上传:%s'%path.data, category='err')
                return redirect(url_for('admin.classify_add'))
            form.cover.data = file_move_to(path.data)
            file_delete(cover)
        db.session.add(field_obj_set(classify, form.data))
        db.session.commit()
        flash('编辑成功!', category='ok')
        return redirect(url_for('admin.classify'))
    title = '编辑分类'
    data = dict(title=title, form=form, id=id, cover=cover)
    return render_template('admin/classify.form.html', **data)