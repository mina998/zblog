# coding:utf-8
import os
from datetime import datetime
from common.configs import UPLOAD_FILE_TEMP_PATH
from common.models import Site


class Uploads():
    __instance = None

    def __init__(self,files, allowed=None):

        if allowed is None: self.__allowed = self.__allowed2()

        self.__path = UPLOAD_FILE_TEMP_PATH
        self.__files = []

        self.err  = 0 # 0没有错误
        self.data = []

        if isinstance(files, list): self.__files = files
        else: self.__files = [files]


    def save(self):
        self.__check_file_allow()
        if self.err == 0:
            for file in self.__files: self.data.append(self.__save(file))
            if len(self.data) == 1: self.data = self.data[0]
            elif len(self.data) < 1: self.data = ''
        return self


    def __check_file_allow(self):
        '''
        检查是否允许上传
        '''
        for file in self.__files:
            # 获取文件名
            filename = file.filename
            # 获取文件扩展名
            sss = filename.rsplit('.', 1)
            extname = sss[1] if len(sss) > 1 else ''
            # 不充许上传类型
            if not (filename and extname in self.__allowed):
                self.data.append(filename)
        # 如果有不充许上传的文件
        if len(self.data) > 0 :
            self.data = '|'.join(self.data)
            self.err = 1


    def __save(self,file):
        '''
        保存文件
        :param file: FileStorage对象
        :return: 返回保存文件路径
        '''
        # 获取文件扩展名
        extname = file.filename.rsplit('.', 1)[1]
        # 生成不重复的文件名
        filename = str(datetime.now().timestamp()).replace('.', '')[-8:] + '.' + extname
        # 生成保存文件夹路径
        folder = self.__path.lstrip('/')
        # 创建文件夹
        if (os.path.exists(folder)) is False: os.makedirs(folder, os.O_RDWR)
        # 生成保存文件地址
        image_save_path = folder + filename
        # 保存文件
        file.save(image_save_path)
        #
        return '/' + image_save_path

    def __allowed2(self):
        allow =  Site.query.filter_by(name='upfiletype').one()
        return allow.value.split('#')


    def __new__(cls, *args, **kwargs):
        if cls.__instance is None: cls.__instance = object.__new__(cls)
        return cls.__instance