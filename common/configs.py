# coding:utf-8

# 修改些配置文件需要重启服务器
# DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = 0
SQLALCHEMY_DATABASE_URI ='sqlite:///sqlite3.db'
# SQLALCHEMY_ECHO = True

# 文件上传大小控制 默认最大上传2M
MAX_CONTENT_LENGTH = 2 * 1024 * 1024
# 文件上传临时保存路径
UPLOAD_FILE_TEMP_PATH = '/static/temp/'
# 文件上传成功后保存路径
UPLOAD_FILE_SAVE_PATH = '/static/uploads/'

SECRET_KEY = 'ce2c0c02d6d8413782794451788ffa7f'

# 验证码插件配置
VAPTCHA_ID = '5c938abafc650ef6e0821e21'
VAPTCHA_SECRET_KEY='f30542001d2f4e438ea3a07bc4184bba'