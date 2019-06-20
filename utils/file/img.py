#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 图片工具类
# @Author : Zackeus
# @File : img.py 
# @Software: PyCharm
# @Time : 2019/3/26 9:56


import os
import piexif
from PIL import Image
from enum import Enum, unique

from utils.assert_util import Assert
from utils import encodes
from utils.file import FileFormat


class ImgUtil(object):

    @staticmethod
    def img_compress(path, threshold=4):
        """
        将图片压缩到指定阀值大小的 base64
        :param path:文件路径
        :param threshold:阀值大小(单位：M)
        :return:
        """
        Assert.is_true(assert_condition=os.path.isfile(path),
                       assert_msg='图片不存在：{0}'.format(path))
        # 阈值换算成比特
        threshold = threshold*1024*1024
        with Image.open(path) as im:
            if os.path.getsize(path) > threshold:
                width, height = im.size
                new_width = 1024
                new_height = int(new_width * height * 1.0 / width)
                resized_im = im.resize((new_width, new_height))
                return encodes.pil_to_base64(resized_im)
            return encodes.pil_to_base64(im)

    @staticmethod
    def loss_less(in_path, out_path, format=FileFormat.JPEG.value):
        """
        图片近无损压缩
        :param in_path:
        :param out_path: 输出目录
        :param format:
        :return:
        """
        Assert.is_true(os.path.isfile(in_path), '图片不存在：{0}'.format(in_path))
        with Image.open(in_path) as img:
            img = img.convert(ImgChannel.RGB.value)
            exif_bytes = piexif.dump({})
            img.save(out_path, format, exif=exif_bytes)


@unique
class ImgChannel(Enum):
    """
    图片色彩通道
    """
    RGB = 'RGB'
    RGBA = 'RGBA'


if __name__ == '__main__':
    filename = 'D:/FileData/c60d0388932211e9a11a5800e36a34d8/Img/c634fdec932211e994335800e36a34d8/1.JPG'
    # base_str = ImgUtil.img_compress(filename)
    # print(base_str)
    # encodes.base64_to_file(base_str,
    #                        'D:/FileData/c60d0388932211e9a11a5800e36a34d8/Img/c634fdec932211e994335800e36a34d8/',
    #                        'zz',
    #                        'JPG')
    ImgUtil.loss_less(filename, filename)