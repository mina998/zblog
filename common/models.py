# coding:utf-8
from datetime import datetime
from common.extends import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


# 定义多对多中间表
tag2post = db.Table(
    'tag2post',
    db.Column('pid', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tid', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Post(Base):
    '''
    文章表
    '''
    __tablename__ = 'post'
    # 文章标题
    title = db.Column(db.String(200), default='')
    # 文章内容
    content = db.Column(db.Text, default='')
    # 关建字
    keywords = db.Column(db.String(100), default='')
    # 描述
    desc = db.Column(db.String(200), default='')
    # 摘要
    summary = db.Column(db.String(200), default='')
    # 允许评论
    is_review = db.Column(db.Integer, default=0, comment='1为禁止评论,0为允许')
    # 密码
    passwd = db.Column(db.String(20), default='', comment='密码')
    # 更新时间
    uptime = db.Column(db.DateTime, default=datetime.now)
    # 作者
    author = db.Column(db.String(20), default='')
    # 浏览数
    view = db.Column(db.Integer, default=0)
    # 文章状态ID
    sid = db.Column(db.Integer, db.ForeignKey("style.id"))
    # 文章分类ID
    cid = db.Column(db.Integer, db.ForeignKey("classify.id"))
    # 关联表
    classify = db.relationship("Classify", backref=db.backref('posts'))
    # 关联表
    reviews = db.relationship("Review", backref=db.backref('posts'))
    # 关联表
    style = db.relationship("Style", backref=db.backref('posts'))

    @staticmethod
    def getPagination(page,cid=None, sid=1, num=10):
        '''
        文章分页查询
        :param page: 页码
        :param cid: 分类id None 查所有分类
        :param sid: 文章类型 1为普通 2为置顶
        :param num: 每页文章条数
        :return: 文章(Post对象)结果集
        '''
        if cid:
            return Post.query.filter(Post.cid == cid).order_by(Post.id.desc()).paginate(page=page, per_page=num)
        return Post.query.filter(Post.sid == sid).order_by(Post.id.desc()).paginate(page=page, per_page=num)

    @staticmethod
    def getTop(cid=None, num=5):
        '''
        置顶文章
        :param cid: 分类id, None代表查所有分类
        :param num: 取文章条数
        :return: 文章(Post对象)结果集
        '''
        if cid:
            return Post.query.filter_by(cid=cid, sid=2).order_by(Post.id.desc()).limit(num).all()
        return Post.query.filter_by(sid=2).order_by(Post.id.desc()).limit(num).all()


class Tag(Base):
    '''
    标签表
    '''
    __tablename__ = 'tag'
    # 标签名字
    name = db.Column(db.String(20), nullable=False, unique=True)
    # 标签点击数
    click= db.Column(db.Integer, nullable=False, default=0, comment='标签点击数')

    # 多对多定义
    posts = db.relationship('Post', secondary='tag2post', backref=db.backref('tags'))

    @staticmethod
    def tags():
        return Tag.query.order_by(Tag.click.desc()).order_by(Tag.id.desc()).limit(15).all()


class Classify(Base):
    '''
    类别表
    '''
    __tablename__ = 'classify'
    # 类别名称
    title = db.Column(db.String(20), nullable=False)
    # 父级ID
    pid = db.Column(db.Integer, default=0)
    # 是否显示在导航栏
    asn = db.Column(db.Integer, default=0, comment='0为显示在导航栏,1为不显示')
    # 分类关键字
    keywords = db.Column(db.String(200), default='')
    # 分类描述
    desc = db.Column(db.String(200), default='')
    # 分类排序
    sort = db.Column(db.Integer, default=1)
    # 封面
    cover = db.Column(db.String(200), default='')


class Review(Base):
    '''
    评论表
    '''
    __tablename__ = 'review'
    # 评论人邮箱
    email = db.Column(db.String(60), default='')
    # 评论内容
    comment = db.Column(db.String(255), nullable=True)
    # 评论人QQ
    qq = db.Column(db.String(20), default='')
    # 评论人昵称
    name = db.Column(db.String(60), default='')
    # 评论时间
    addtime = db.Column(db.DateTime, default=datetime.now)
    # @人
    at = db.Column(db.Text, default='')
    # 禁止显示
    ban = db.Column(db.Integer, default=0, comment='1为不显示')
    # 所属文章ID
    pid = db.Column(db.Integer, db.ForeignKey("post.id"))


class Style(Base):
    __tablename__ = 'style'
    name = db.Column(db.String(60), nullable=True)


class Site(Base):
    '''
    站点信息表
    '''
    __tablename__ = 'site'
    # 站点字段
    name = db.Column(db.String(60), nullable=False)
    # 字段别名
    alias = db.Column(db.String(60), nullable=False)
    # 字段值
    value = db.Column(db.String(500), default='')
    # 字段分组
    group = db.Column(db.String(20), nullable=False)
