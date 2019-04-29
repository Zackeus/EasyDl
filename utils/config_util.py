#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 配置文件工具类
# @Author : Zackeus
# @File : config.py 
# @Software: PyCharm
# @Time : 2019/4/3 14:20

import os
import configparser
from utils.encodes import Unicode


class ConfigUtils(configparser.ConfigParser):
    """
    基础读取配置文件
    -read(filename)         直接读取文件内容
    -sections()             得到所有的section，并以列表的形式返回
    -options(section)       得到该section的所有option
    -items(section)         得到该section的所有键值对
    -get(section,option)    得到section中option的值，返回为string类型
    -getint(section,option) 得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数
    """

    # 缓存
    __file_dict = {}

    def __init__(self, path):
        """
        实例化
        :param path:文件路径
        """
        super(self.__class__, self).__init__()
        self.path = path
        self.read(filenames=path, encoding=Unicode.UTF_8.value)

    def get_config_dict(self):
        """
        获取资源配置文件，形成字典
        :return:
        """
        if self.path not in self.__file_dict:
            d = dict(self._sections)
            for k in d:
                d[k] = dict(d[k])
            self.__file_dict[self.path] = d
        return self.__file_dict.get(self.path)

    def get_config_value(self, prop_name):
        """
        获取资源文件，形成字典，获取属性值
        :param prop_name: 属性名称
        :return: 返回字符串格式的属性值
        """
        return self.get_config_dict().get(prop_name)

    def get_sections(self):
        """
        获取所有的sections
        :return:
        """
        return self.sections()

    def get_options(self, section):
        """
        获取section下所有的key
        :param section:
        :return:
        """
        return self.options(section=section)

    def get_kvs(self, section):
        """
        获取section下所有的键值对
        :param section:
        :return:
        """
        return self.items(section=section)

    def get_key_value(self, section, option):
        """
        根据section和option获取指定的value
        :param section:
        :param option:
        :return:
        """
        return self.get(section=section, option=option)


if __name__ == '__main__':
    base_dir = os.path.abspath(path=os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base_dir, 'static', 'db.cfg')

    cf = ConfigUtils(path=path)
    sections = cf.get_sections()
    print(sections)
    print(cf.get_options(section=sections[0]))
    print(cf.get_kvs(section=sections[0]))
    print(cf.get_key_value(section=sections[0], option='port'))
    print(cf.get_config_dict())
    print(cf.get_config_value('pymssql'))


