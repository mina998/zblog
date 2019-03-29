# coding:utf-8
from common.models import Classify


class Breadcrumb:
    __instance = None
    def __init__(self, obj=None):
        self.__bd = []
        self.obj = obj

    def get(self):
        # 首页
        index = {'args': dict(endpoint='home.index'), 'title': '首页'}
        # 如果对象为空 设置为首页
        if self.obj is None: return [index]
        # 对象Post
        if self.obj.__class__.__name__ == 'Post':
            args = dict(id=self.obj.id, title=self.obj.title, endpoint='home.post')
            self.__classify(self.obj.classify)
            self.__bd.append({'args': args, 'title': self.obj.title})
        # 对象 Classify
        if isinstance(self.obj, Classify):
            self.__classify(self.obj)
        # 对象 Tag
        if self.obj.__class__.__name__ == 'Tag':
            args = dict(id=self.obj.id, name=self.obj.name, endpoint='home.tag')
            self.__bd.append({'args': args, 'title': self.obj.name})

        self.__bd.insert(0, index)
        return self.__bd

    def __classify(self, classify):
        '''
        添加当前分类 递归查询所有上级分类
        :return:
        '''
        args = dict(id=classify.id, title=classify.title, page=1, endpoint='home.classify')
        self.__bd.insert(0, {'args': args, 'title': classify.title})

        self.__query(classify)

    def __query(self, classify):
        '''
        查询上级分类
        :param classify: Classify实例对象
        :return:
        '''
        if classify.pid > 0:
            obj = Classify.query.get(classify.pid)
            arg = dict(id=obj.id, title=obj.title, page=1, endpoint='home.classify')
            self.__bd.insert(0, {'args': arg, 'title': obj.title})
            self.__query(obj)


    def __new__(cls, *args, **kwargs):
        if cls.__instance is None: cls.__instance = object.__new__(cls)
        return cls.__instance

