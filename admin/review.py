# coding:utf-8
from admin import admin
from flask import render_template, request, flash, redirect, url_for
from common.extends import db
from common.models import Review


@admin.route('/review')
def review():
    title= '评论管理'
    page = request.args.get('page', 1, type=int)
    viee = Review.query.order_by(Review.id.desc()).paginate(page=page, error_out=False)
    args = dict(endpoint='admin.review')
    data = dict(title=title, pagination=viee, args=args)
    return render_template('admin/review.html', **data)


@admin.route('/review/del', methods=['GET', 'POST'])
def review_del():
    id = request.args.get('id',0)
    if id and id.isdigit(): ids=[id]
    if request.method=='POST': ids = [id for id in request.form.getlist('id') if id.isdigit()]
    ids = ','.join(ids)
    if len(ids) > 0:
        db.session.execute('delete from review where id in (%s)'%ids)
        db.session.commit()
        flash('删除成功!', category='ok')
    return redirect(url_for('admin.review'))


@admin.route('/review/up/')
def review_up():
    all = request.args.get('all',0)
    ids = [id for id in all.split(',') if id.isdigit()]
    if len(ids) > 0:
        ids = ','.join(ids)
        sql = 'update review set ban = 1 where id in (%s)'% ids
        db.session.execute(sql)
        db.session.commit()
        flash('操作成功!', category='ok')
    return redirect(url_for('admin.review'))


@admin.route('/review/allow/<int:id>')
def review_allow(id):
    if Review.query.filter_by(id=id).update(dict(ban=0)):
        db.session.commit()
        flash('操作成功!', category='ok')
    return redirect(url_for('admin.review'))