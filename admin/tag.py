# coding:utf-8
from admin import admin
from flask import render_template, request, flash, redirect, url_for
from admin.forms.tag import TagForm
from common.extends import db
from common.models import Tag


@admin.route('/tag')
def tag():
    title= '标签管理'
    page = request.args.get('page', 1, type=int)
    tags = Tag.query.order_by(Tag.click.desc()).order_by(Tag.id.desc()).paginate(page=page, error_out=False)
    args = dict(endpoint='admin.tag')
    data = dict(title=title, pagination=tags, args=args)
    return render_template('admin/tag.html', **data)


@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
def tag_edit(id):
    tag  = Tag.query.get_or_404(id)
    form = TagForm(data={'name':tag.name})
    title= '标签编辑'

    if form.validate_on_submit():
        tag.name = form.data.get('name')
        db.session.commit()
        flash('编辑成功!', category='ok')
        return redirect(url_for('admin.tag'))

    data = dict(tag=tag, form=form, title=title)
    return render_template('admin/tag.form.html', **data)


@admin.route('/tag/del', methods=['GET', 'POST'])
def tag_del():

    id = request.args.get('id')

    if id is not None and id.isdigit(): ids=[id]

    if request.method=='POST': ids = [id for id in request.form.getlist('id') if id.isdigit()]

    ids = ','.join(ids)

    db.session.execute('delete from tag where id in (%s)'%ids)

    db.session.commit()

    flash('删除成功!', category='ok')
    return redirect(url_for('admin.tag'))