# coding:utf-8
import re
from flask import render_template, request, jsonify, g, flash, redirect, url_for, session

from common.extends import db
from common.models import Site, Post, Classify, Review, Tag
from common.util import site_to_dict
from home import home
from home.forms import ReviewForm, LoginForm
from home.weigets import Breadcrumb


@home.route('/')
def index():
    site = Site.query.filter_by(group='seo').all()
    page = request.args.get('page', 1, type=int)
    post = Post.getPagination(page, num=10)
    data = dict(breadcrumb=Breadcrumb().get(), gtop=Post.getTop(), main=site_to_dict(site), pagination=post)
    return render_template('home/index.html', **data)

@home.route('/<title>.c<int:id>.p<int:page>')
def classify(title, id, page):
    post = Post.getPagination(page, cid=id)
    main = Classify.query.get(id)
    gtop = Post.getTop(cid=id, num=3)
    args = dict(endpoint='home.classify', title=title, id=id)
    data = dict(pagination=post, gtop=gtop, breadcrumb=Breadcrumb(main).get(), args=args, main=main)
    return render_template('home/classify.html', **data)

@home.route('/<title>.p<int:id>.html', methods=['GET','POST'])
def post(title, id):
    form = ReviewForm()
    main = Post.query.get_or_404(id)

    g.view_post_passwd = ''
    if request.method == 'POST' and request.form.get('passwd2') != main.passwd:
        flash('查看密码不正确!', category='err')
    if request.form.get('passwd2') == main.passwd:
        g.view_post_passwd = main.passwd

    data = dict(main=main, breadcrumb=Breadcrumb(main).get(), form=form)
    Post.query.filter_by(id = id).update({"view": main.view + 1})
    db.session.commit()
    return render_template('home/post.html', **data)

@home.route('/post/reviews/<int:pid>', methods=['POST'])
def post_reviews(pid):
    status = 1  # 前台接收状态
    action = 'false' #前台跳转地址
    f = Post.query.get_or_404(pid)
    if f.is_review == 1: return jsonify(dict(status=1, msg={'comment':['此篇文章不充许评论']}, action=action))

    form = ReviewForm()
    comment = form.data.get('comment')

    pat = re.compile(r'(<a\shref="#at(\d+?)">@([a-zA-Z0-9_\u4e00-\u9fa5\s·]+?)</a>)')
    res = pat.findall(comment)
    ats = []

    comment = re.sub(pat,'',comment)
    comment = re.sub(r'&nbsp;[\s\n]*&nbsp;','',comment)

    for at in res:
        if Review.query.filter_by(name=at[2], id=at[1]).first(): ats.append(at[0])

    if form.validate_on_submit():
        if not comment.replace('&nbsp;','').strip():
            return '{"status":"1", "msg":{"comment":["评论内容不能为空!"]}, "action":"false"}'
        review = Review(
            name   = form.data.get('name').strip(),
            email  = form.data.get('email').strip(),
            comment= comment,
            at     = '&nbsp;'.join(list(set(ats))),
            pid    = pid
        )
        db.session.add(review)
        db.session.flush()
        action = review.id
        db.session.commit()
        status = 0

    data = dict(
        status = status,
        msg = form.errors,
        action = action
    )
    return jsonify(data)

@home.route('/<name>.t<int:id>')
def tag(name,id):
    main = Tag.query.get_or_404(id)
    main.title = main.name
    data = dict(main=main, gtop=Post.getTop(), breadcrumb=Breadcrumb(main).get())
    return render_template('home/tag.html', **data)

@home.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        obj = Site.query.filter(Site.name.in_(['username','password','nikename'])).all()
        user = site_to_dict(obj)
        if user['username'] == form.data.get('username') and user['password'] == form.data.get('password'):
            session['login'] = 1
            session['nikename'] = user['nikename']
            return redirect(url_for('admin.index'))
        else:
            flash('帐户或者密码不正确!', category='err')
            return redirect('/login')
    return render_template('/home/login.html',form=form)