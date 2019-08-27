#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 图片工具类
# @Author : Zackeus
# @File : img.py 
# @Software: PyCharm
# @Time : 2019/3/26 9:56


import numpy as np
import cv2
import os
import piexif
from PIL import Image, ImageEnhance
from enum import Enum, unique
from pngquant.main import PngQuant as BasePngQuant

from utils.assert_util import Assert
from utils.file import FileFormat


class ImgUtil(object):

    @staticmethod
    def get_img_pixel(path):
        """
        获取图片像素大小
        :param path:
        :return:
        """
        Assert.is_true(os.path.isfile(path), '图片不存在：{0}'.format(path))
        with Image.open(path) as i:
            return i.size

    @staticmethod
    def img_compress(path, threshold=4):
        """
        将图片压缩到指定阀值大小的 base64
        :param path:文件路径
        :param threshold:阀值大小(单位：M)
        :return:
        """
        from utils.encodes import pil_to_base64
        # 阈值换算成比特
        _threshold = threshold * 1024 * 1024
        Assert.is_true(os.path.isfile(path), '图片不存在：{0}'.format(path))
        w, h = ImgUtil.get_img_pixel(path)

        with Image.open(path) as im:
            if w * h > _threshold:
                new_width = 1024
                new_height = int(new_width * h * 1.0 / w)
                resized_im = im.resize((new_width, new_height))
                return pil_to_base64(resized_im)
            return pil_to_base64(im)

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

    @staticmethod
    def change_size(read_file):
        image = cv2.imread(read_file, 1)  # 读取图片 image_name应该是变量

        b = cv2.threshold(image, 15, 255, cv2.THRESH_BINARY)  # 调整裁剪效果
        binary_image = b[1]  # 二值图--具有三通道
        binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
        print(binary_image.shape)  # 改为单通道

        x = binary_image.shape[0]
        print("高度x=", x)
        y = binary_image.shape[1]
        print("宽度y=", y)
        edges_x = []
        edges_y = []

        for i in range(x):

            for j in range(y):

                if binary_image[i][j] == 255:
                    # print("横坐标",i)
                    # print("纵坐标",j)
                    edges_x.append(i)
                    edges_y.append(j)

        left = min(edges_x)  # 左边界
        right = max(edges_x)  # 右边界
        width = right - left  # 宽度

        bottom = min(edges_y)  # 底部
        top = max(edges_y)  # 顶部
        height = top - bottom  # 高度

        pre1_picture = image[left:left + width, bottom:bottom + height]  # 图片截取

        return pre1_picture  # 返回图片数据


class PngQuant(BasePngQuant):

    def __init__(self,
                 quant_file=None,
                 min_quality=None,
                 max_quality=None,
                 ndeep=None,
                 ndigits=None,
                 tmp_file=None):
        """
        png 图片无损压缩
        :param quant_file:
        :param min_quality:
        :param max_quality:
        :param ndeep:
        :param ndigits:
        :param tmp_file:
        """
        super(self.__class__, self).__init__()
        super().config(quant_file, min_quality, max_quality, ndeep, ndigits, tmp_file)


class Enhancer:

    def enhance(self, path, bright=True, color=True, contrast=True, sharp=True, gamma=True):
        """
        图片增强
        :param path:
        :param bool bright:
        :param bool color:
        :param bool contrast:
        :param bool sharp:
        :param bool gamma:
        :return:
        """
        im = cv2.imread(filename=path)
        if bright:
            im = self.bright(im)
        if color:
            im = self.color(im)
        if contrast:
            im = self.contrast(im)
        if sharp:
            im = self.sharp(im)
        if gamma:
            im = self.gamma(im)
        cv2.imwrite(filename=path, img=im)

    def bright(self, image, brightness=0.8):
        """
        调整图像宽度
        :param image:
        :param float brightness: 亮度增强因子(0.0将产生黑色图像；为1.0将保持原始图像)
        :return:
        """
        enh_bri = ImageEnhance.Brightness(image)
        imageBrightend = enh_bri.enhance(brightness)
        return imageBrightend

    def color(self, image, color=0.8):
        """
        调整图像颜色
        :param image:
        :param float color: 颜色增强因子(1.0为原始图像)
        :return:
        """
        enh_col = ImageEnhance.Color(image)
        color = color
        imageColored = enh_col.enhance(color)
        return imageColored

    def contrast(self, image, contrast=0.8):
        """
        调整图像对比度
        :param image:
        :param float contrast: 0.0将产生纯灰色图像；为1.0将保持原始图像
        :return:
        """
        enh_con = ImageEnhance.Contrast(image)
        contrast = contrast
        image_contrasted = enh_con.enhance(contrast)
        return image_contrasted

    def sharp(self, image, sharpness=2.0):
        """
        调整图像锐度
        :param image:
        :param float sharpness: 0.0将产生模糊图像；为1.0将保持原始图像，为2.0将产生锐化过的图像
        :return:
        """
        enh_sha = ImageEnhance.Sharpness(image)
        sharpness = sharpness
        image_sharped = enh_sha.enhance(sharpness)
        return image_sharped

    def gamma(self, image, gamma=1.35):
        """
        图像伽马矫正
        :param image:
        :param float gamma:
        :return:
        """
        gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(image, gamma_table)


@unique
class ImgChannel(Enum):
    """
    图片色彩通道
    """
    RGB = 'RGB'
    RGBA = 'RGBA'


if __name__ == '__main__':
    # filename = 'D:/FileData/d03544f8932a11e9b7219032c5b02716/Img/d056a5da932a11e9a5d19032c5b02716/10.JPG'
    # base_str = ImgUtil.img_compress(filename)
    # print(base_str)
    # encodes.base64_to_file(base_str,
    #                        'D:/FileData/c60d0388932211e9a11a5800e36a34d8/Img/c634fdec932211e994335800e36a34d8/',
    #                        'zz',
    #                        'JPG')

    # ********** 去黑边 ************************
    # source_path = "D:/FileData/b581429296fe11e9bab69032c5b02716/Img/b606c64696fe11e9848b9032c5b02716/"  # 图片来源路径
    # save_path = "D:/FileData/b581429296fe11e9bab69032c5b02716/Img/1/"  # 图片修改后的保存路径
    #
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    #
    # file_names = os.listdir(source_path)
    #
    # for i in range(len(file_names)):
    #     x = ImgUtil.change_size(source_path + file_names[i])  # 得到文件名
    #     cv2.imwrite(save_path + file_names[i], x)
    #     print("裁剪：", file_names[i])
    #     print("裁剪数量:", i)

    # *********** PNG 图片压缩, 需要配置pngquant.exe 环境变量
    pngquant = PngQuant(min_quality=80, max_quality=100)
    pngquant.quant_image('D:/FileData/1.JPG')

    # *********** 图片增强
    # Enhancer().enhance('E:/FileData/1.png', False, False, False, False, True)


