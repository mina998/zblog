# coding:utf-8
from flask import Blueprint, request

from common.configs import VAPTCHA_ID
from common.extends import db

from common.models import Classify, Site, Post, Review, Tag
from common.util import site_to_dict

home = Blueprint('home', __name__)

def getHot(cid=None, num=10):
    '''
    浏览最多文章
    :param cid: 分类id, None代表查所有分类
    :param num: 取文章条数
    :return: 文章(Post对象)结果集
    '''
    # if cid:
    #     return Post.query.filter_by(cid=cid).order_by(Post.view.desc()).limit(num).all()
    return Post.query.order_by(Post.view.desc()).limit(num).all()


def getTag(cid=None, num=10):
    return Tag.query.order_by(Tag.click.desc()).limit(num).all()


def vaptcha(width=None, height=None):
    data = dict(
        id = VAPTCHA_ID,
        width = width+'px' if width else 'auto',
        height = height+'px' if height else 'auto',
    )
    return data


def getReviews(num=10):
    '''
    评论最多文章
    :param num: 取文章条数
    :return: 结果集
    '''
    sub = db.func.count(Review.pid)
    return db.session.query(Post.title, sub.label('rn'),Post.id).join(Review).group_by(Review.pid).order_by(sub.desc()).limit(num).all()


@home.context_processor
def common():
    # 导航
    nav = Classify.query.filter(Classify.asn < 1).order_by(Classify.sort).all()
    # 网站
    site = Site.query.filter_by(group='site').all()
    # 网站名字
    name = Site.query.filter_by(name='title').first()

    webname = name.value if name else '网站名称'

    data = dict(
        site=site_to_dict(site),
        nav=nav,
        webname=webname,
        hot=getHot,
        reviews=getReviews,
        wtag=getTag,
        vaptcha=vaptcha
    )
    return data

@home.before_request
def webs_witch():
    site = Site.query.filter(Site.name.in_(['switch','mark'])).all()
    site = site_to_dict(site)
    if request.path == '/login': return None
    if site['switch'] == '2': return site['mark']

from home import views
