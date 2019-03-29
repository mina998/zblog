# coding:utf-8
def site_to_dict(list):
    '''
    Site 表数据转换
    :param list: Site对象 数据列表
    :return: 字典
    '''
    data = {}
    for obj in list:
        data[obj.name] = obj.value
    return data
