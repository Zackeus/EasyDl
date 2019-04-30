#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 编码解码工具类
# @Author : Zackeus
# @File : encodes.py 
# @Software: PyCharm
# @Time : 2019/3/26 9:57


import random
import os
import base64
import cv2
import numpy as np
import re
from Crypto.Cipher import AES
from io import BytesIO
from PIL import Image
from enum import Enum, unique

from utils.file.file import FileUtil
from utils.object_util import is_not_empty
from utils.assert_util import Assert


def file_to_base64(file):
    """
    文件转base64
    :param file:文件路径
    :return:
    """
    with open(file=file, mode='rb') as f:
        return str(base64.b64encode(s=f.read()), encoding=Unicode.UTF_8.value)


def base64_to_file(base64_str, file_dir, file_name, file_format):
    """
    base64还原文档
    :type file_format: str
    :param base64_str: 文档base64字符
    :param file_dir: 文件目录
    :param file_name: 文件名
    :param file_format: 文件格式
    :return:
    """
    FileUtil.creat_dirs(file_dir)
    if file_format.startswith(os.curdir):
        file = file_name + file_format
    else:
        file = os.curdir.join([file_name, file_format])
    file_path = os.path.join(file_dir, file)
    with open(file=file_path, mode='wb') as f:
        f.write(base64.b64decode(s=base64_str))
    return FileUtil.normcase(file_path)


def base64_to_cv_np(base64_str):
    """
    base64字符转cv格式的numpy
    :param base64_str:
    :return:
    """
    if base64 is None:
        return None
    bytes_code = base64.b64decode(s=base64_str)
    np_array = np.fromstring(string=bytes_code, dtype=np.uint8)
    # 转换Opencv格式; opencv 使用的是 BGR，所以要转换
    img = cv2.imdecode(buf=np_array, flags=cv2.COLOR_BGR2RGB)
    return img


def cv_np_to_base64(cv_np, format='.jpg'):
    """
    cv格式的numpy转base64字符
    :param cv_np:
    :param format:图片格式
    :return:
    """
    if cv_np is None:
        return None
    res = cv2.imencode(ext=format, img=cv_np)
    return base64.b64encode(res[1]).decode()


def pil_to_base64(pil_img, format='png'):
    """
    PIL.Image 转 base64
    :param pil_img:
    :param format:
    :return:
    """
    output_buffer = BytesIO()
    pil_img.save(output_buffer, format=format)
    byte_data = output_buffer.getvalue()
    return str(base64.b64encode(byte_data), encoding=Unicode.UTF_8.value)


def base64_to_pil(base64_str):
    """
    base64 转 PIL.Image
    :param base64_str:
    :return:
    """
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    with Image.open(image_data) as img:
        return img


def hash_code(hash_cls, hexadecimal=True, b64=False):
    """
    哈希编码
    :param hash_cls: 哈希实例
    :param hexadecimal: 是否使用十六进制，否则使用二进制
    :param b64: 是否 base64 编码
    :return:
    """
    hash_str = hash_cls.hexdigest() if hexadecimal else hash_cls.digest()
    hash_str = base64.b64encode(hash_str).decode(Unicode.UTF_8.value) if b64 else hash_str
    return hash_str

@unique
class Unicode(Enum):
    GBK = 'GBK'
    UTF_8 = 'UTF-8'
    UTF_16 = 'UTF-16'


class AESUtil(object):

    __source = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz123456789'

    def __init__(self, key):
        """

        :param key: 秘钥
        """
        Assert.is_true(is_not_empty(key), 'AES 秘钥不能为空')
        self.key = key

    @classmethod
    def get_key(cls, n):
        """
        获取密钥 n 密钥长度
        :return:
        """
        c_length = int(n)

        length = len(cls.__source) - 1
        result = ''
        for i in range(c_length):
            result += cls.__source[random.randint(0, length)]
        return result

    def _pkcs7_padding(self, text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding=Unicode.UTF_8.value))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if(bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding) * padding
        return text + padding_text

    def _pkcs7_unpadding(self, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        un_padding = ord(text[length-1])
        return text[0:length - un_padding]

    def encrypt(self, content):
        """
        AES加密,key,iv使用同一个,模式cbc,填充 pkcs7
        :param content: 加密内容
        :return:
        """
        key_bytes = bytes(self.key, encoding=Unicode.UTF_8.value)
        iv = key_bytes
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # 处理明文
        content_padding = self._pkcs7_padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding=Unicode.UTF_8.value))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding=Unicode.UTF_8.value)
        return result

    def decrypt(self, content):
        """
        AES解密, key,iv使用同一个,模式cbc,去填充pkcs7
        :param content:
        :return:
        """
        key_bytes = bytes(self.key, encoding=Unicode.UTF_8.value)
        iv = key_bytes
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # base64解码
        encrypt_bytes = base64.b64decode(content)
        # 解密
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        # 重新编码
        result = str(decrypt_bytes, encoding=Unicode.UTF_8.value)
        # 去除填充内容
        result = self._pkcs7_unpadding(result)
        return result


if __name__ == '__main__':
    # with open(file='../imageCorrect/data/18.jpg', mode='rb') as f:
    #     base64_code = base64.b64encode(f.read())
    # cv2.imshow("org", base64_to_cv_np(base64_code))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # cv 转 base 64
    # image = cv2.imread('../imageCorrect/data/18.jpg')
    # base_str = cv_np_to_base64(image)
    # base64_to_file(base64_str=base_str, file='./data/2.jpg')

    # AES 加解密
    # aes = AESUtil(AESUtil.get_key(16))
    # aes_str = aes.encrypt('D:/贷后资料/一阶/4月26日15时之前/张舟341125199503200032H-a43da59467c511e9a99d5800e36a34d8/IMG/a450ed6e67c511e98a375800e36a34d8/4.PNG')
    # print(aes_str)
    # decode_str = aes.decrypt(aes_str)
    # print(decode_str)

    # base_str = file_to_base64('D:/贷前资料/05121ff8230511e997a8a164741611fd/png/1.png')
    # print(type(base_str))
    # base64_to_file(base_str, 'D:/贷前资料/test.png')

    print(AESUtil.get_key(16))



