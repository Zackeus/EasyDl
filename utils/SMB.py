#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 基于SMB共享文件操作工具类
# @Author : Zackeus
# @File : smb.py 
# @Software: PyCharm
# @Time : 2019/3/26 10:04


from smb.SMBConnection import SMBConnection
from utils.assert_util import Assert


class SMB(SMBConnection):

    def __init__(self, username, password, my_name, remote_name, ip, service_name, timeout=60):
        """
        初始化 smb 访问对象
        :param username:用户名
        :param password:密码
        :param my_name:本地的NetBios Name
        :param remote_name:远端的NetBios Name
        :param ip:远程IP
        :param service_name:共享空间(如 'shares')
        :param timeout:超时(可以为空默认60)')
        """
        super(self.__class__, self).__init__(username=username,
                                             password=password,
                                             my_name=my_name,
                                             remote_name=remote_name)
        self.service_name = service_name
        self.conn = self.connect(ip=ip, timeout=timeout)

    def is_success(self):
        """
        远程连接是否成功
        :rtype:bool
        :return:
        """
        return self.conn

    def get_file_list(self, path):
        """
        获取文件列表
        :param path:文件目录所在文件夹
        :return:文件对象组成的元组,注意返回结果里面包含所有文件甚至是 . 和 .. 也会包含进去
        """
        Assert.is_true(assert_condition=self.is_success(), assert_msg='SMB连接失败...')
        return self.listPath(service_name=self.service_name, path=path)

    def down_file(self, local_file, remote_file):
        """
        下载文件到本地
        :param local_file:本地文件路径
        :param remote_file:远程文件路径
        :return:
        """
        Assert.is_true(assert_condition=self.is_success(), assert_msg='SMB连接失败...')
        with open(file=local_file, mode='wb') as f:
            self.retrieveFile(service_name=self.service_name, path=remote_file, file_obj=f)

    def upload_file(self, local_file, remote_file):
        """
        上传文件到服务器
        :param local_file:本地文件路径
        :param remote_file:远程文件路径
        :return:
        """
        Assert.is_true(assert_condition=self.is_success(), assert_msg='SMB连接失败...')
        with open(file=local_file, mode='rb') as f:
            self.storeFile(service_name=self.service_name, path=remote_file, file_obj=f)


if __name__ == '__main__':
    # 初始化一个 smb 访问对象
    samba = SMB(username='it01', password='bnm,./789', my_name='YF-5117', remote_name='FILESERVER',
                ip='10.5.61.6', service_name='shares')
    # 返回True/False
    print(samba.is_success())
    # 获取文件列表
    files = samba.get_file_list(path='征信报告存档文件夹/OA附件')
    for file in files:
        print(file.filename)

    # 下载文件到本地
    # samba.down_file(local_file='D:/AIData/test.pdf',
    #                 remote_file='贷前资料邮箱\Br-A138667000李帅邯郸盛福贷前资料\Br-A138667000李帅邯郸盛福贷前资料.pdf')

    # 上传文件到服务器
    samba.upload_file(local_file='D:/AIData/test.pdf', remote_file='征信报告存档文件夹/OA附件/test.pdf')
