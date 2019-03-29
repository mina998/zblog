# coding:utf-8
import os, shutil
from datetime import datetime
from re import findall
from common.configs import UPLOAD_FILE_TEMP_PATH, UPLOAD_FILE_SAVE_PATH
from common.extends import db
from common.models import Tag


def to_dict(form, obj):
    '''
    数据对象转字典
    :param form: form: FlaskForm表单类
    :param obj: 数据对象 Model对象
    :return: 字典
    '''
    data = dict()
    for key, value in obj.__dict__.items():
        if hasattr(form, key): data[key] = value
    return data

def field_obj_set(obj, form_data):
    '''
    设置数据对象属性字段
    :param obj: Model数据对象
    :param form_data: 表单数据字典
    :return: 数据对象
    '''
    for key, value in form_data.items():
        if hasattr(obj, key): setattr(obj, key, value)
    return obj

def file_delete(files):
    '''
    删除文件,只删除相对路径下的文件
    :param files: 要删除的文件列表或文件
    :return:
    '''
    if not isinstance(files,list) : files = [files]
    for item in files:
        file = item.strip('/')
        if (os.path.isfile(file)): os.remove(file)

        folder = os.path.dirname(file).strip('/')
        # 如果是目录 并且目录下没有文件 就删除
        if os.path.exists(folder) and not os.listdir(folder): os.rmdir(folder)

def find_file_links(content):
    '''
    正则匹配内容中的链接
    :param content: 内容字符串
    :return: 链接列表
    '''
    pattern = r'src="(/static/[\.\w\d/]*?)"'
    return findall(pattern, content)

def file_move_to(file):
    '''
    移动临时文件到保存目录
    :param file: 需要移动的文件相对路径
    :return: 文件相对路径
    '''
    temp = UPLOAD_FILE_TEMP_PATH
    save = UPLOAD_FILE_SAVE_PATH.lstrip('/')
    if file.startswith(temp) and os.path.isfile(file.strip('/')):
        # 生成文件夹路径
        folder = save + datetime.now().strftime("%Y%m%d")+'/'
        # 创建文件夹
        if (os.path.exists(folder)) is False: os.makedirs(folder, os.O_RDWR)

        dis = folder + file.replace(temp,'')
        src = file.lstrip('/')
        shutil.move(src, dis)  # 移动文件
        file_delete(src) # 删除空文件夹 或 文件
        return '/'+dis
    return file

def content_file_handle(content, old_content=None):
    '''
    处理内容中的链接
    :param content: 需要处理的内容
    :return: 处理后的内容
    '''
    content = content if content else ''
    old_content = old_content if old_content else ''

    new_links = find_file_links(content)
    old_links = find_file_links(old_content)
    del_links = list(set(old_links) - set(new_links))
    file_delete(del_links)

    for file in new_links:
        link = file_move_to(file)
        content = content.replace(file,link)
    return content

def tags_handle(new,old=''):
    '''
    处理文章标签
    :param new: 新提交的标签字符串
    :param old: 旧标签字符串,为文章更新提交之前的
    :return:
    '''
    objs = []
    new = set([tag for tag in new.split(',') if tag.strip()]) # 新提交的标签字符串
    old = set([tag for tag in old.split(',') if tag.strip()]) # 旧标签字符串,一般为更新之前的字符串
    els = list(old-new) #获取差积删除

    # 创建Tag表数据对象
    for name in list(new):
        # 查询数据
        tag = Tag.query.filter(Tag.name == name).first()
        if tag is None: tag = Tag(name=name)
        objs.append(tag)

    # 删除无文章引用标签
    for name in els:
        tag = Tag.query.filter_by(name = name).first()
        if len(tag.posts) <= 1: db.session.delete(tag)

    return objs

