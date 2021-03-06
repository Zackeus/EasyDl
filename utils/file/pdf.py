#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : pdf 工具类
# @Author : Zackeus
# @File : pdf.py 
# @Software: PyCharm
# @Time : 2019/3/26 10:00


import os
import fitz
from fitz.fitz import Page

from utils.file import FileUtil, FileFormat, Enhancer, PngQuant
from utils.object_util import is_not_empty
from utils.assert_util import Assert


class PDFUtil(object):

    @staticmethod
    def pdf_to_pic(path, pic_dir, format=FileFormat.JPG.value, loss=True, gamma=True, zoom=210,
                   min_size=1.50, max_size=15.0):
        """
        从pdf中提取图片
        :param path: pdf的路径
        :param pic_dir: 图片保存的路径
        :param format: 图片格式
        :param bool loss: 是否压缩
        :param bool gamma: 是否 gamma 矫正
        :param int zoom: 保存图片分辨率
        :param min_size: 文件大小最小阈值
        :param max_size: 文件大小最大阈值
        :return: {page_num, success_num, fail_num, msg}
        """
        Assert.is_true(os.path.isfile(path), '文件不存在, path: {0}'.format(path))
        page_num, success_num, fail_num = 0, 0, 0
        detail_info = {'images': []}
        pdf = None
        # 初始化图片压缩
        pngquant = PngQuant(min_quality=80, max_quality=100, tmp_file=os.path.join(pic_dir, 'quant.tmp.png'))

        try:
            FileUtil.creat_dirs(pic_dir)
            pdf = fitz.Document(path)
            page_num = pdf.pageCount

            for pg in range(page_num):
                pg_zoom = zoom
                pm_dict = {'page_code': pg + 1}
                try:
                    page = pdf[pg]  # type: Page
                    trans = fitz.Matrix(pg_zoom / 100.0, pg_zoom / 100.0).preRotate(0)
                    pm = page.getPixmap(matrix=trans, alpha=False)                                # 获得每一页的流对象
                    page_path = FileUtil.path_join(pic_dir, '{0}.{1}'.format((pg + 1), format))   # 图片路径
                    pm.writeImage(page_path)                                                      # 保存图片

                    file_size = FileUtil.get_file_size(page_path)
                    if file_size <= min_size:
                        # 低于最小阀值
                        pg_zoom = zoom * 2
                        trans = fitz.Matrix(pg_zoom / 100.0, pg_zoom / 100.0).preRotate(0)
                        pm = page.getPixmap(matrix=trans, alpha=False)
                        pm.writeImage(page_path)
                    elif file_size >= max_size:
                        # 大于最大阀值
                        pg_zoom = zoom * 2 / 3
                        trans = fitz.Matrix(pg_zoom / 100.0, pg_zoom / 100.0).preRotate(0)
                        pm = page.getPixmap(matrix=trans, alpha=False)
                        pm.writeImage(page_path)

                    if gamma:
                        # gamma 矫正
                        Enhancer().enhance(page_path, False, False, False, False, True)

                    if loss:
                        # 对图片进行近无损压缩
                        pngquant.quant_image(page_path)

                    pm_dict['img_path'] = page_path
                    success_num = success_num + 1
                except Exception as e:
                    page_path = pm_dict.get('img_path', '')
                    if is_not_empty(page_path):
                        pm_dict.pop('img_path')
                    if os.path.isfile(page_path):
                        # 处理失败，删除失败文件
                        FileUtil.del_file(page_path)
                    pm_dict['error_msg'] = repr(e) if repr(e) else 'pdf转图片失败'
                    fail_num = fail_num + 1
                finally:
                    detail_info.get('images').append(pm_dict)
        except Exception as e1:
            detail_info['error_msg'] = repr(e1) if repr(e1) else '处理pdf失败'
        finally:
            if is_not_empty(pdf):
                pdf.close()
        if success_num + fail_num != page_num:
            fail_num = page_num - success_num
        return page_num, success_num, fail_num, detail_info


if __name__ == '__main__':
    print(PDFUtil.pdf_to_pic('D:/FileData/3/11.pdf',
                             'D:/FileData/3/jpg',
                             loss=True,
                             gamma=True,
                             size_threshold=1.50))


