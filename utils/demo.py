#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : demo.py 
# @Software: PyCharm
# @Time : 2019/6/3 8:52


import cv2
import imutils
import numpy as np
from utils.file.img import Enhancer
from imutils.perspective import four_point_transform


def pre_process(image):
    ratio = image.shape[0] / 500.0
    image = imutils.resize(image, height=500)

    # 二值化
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 高斯滤波
    gauss_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # 获取自定义核 第一个参数MORPH_RECT表示矩形的卷积核
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3, 3))
    # 膨胀操作 实现过程中发现，适当的膨胀很重要
    dilate_image = cv2.dilate(gauss_image, element)

    # 边缘提取
    # edged_image = cv2.Canny(gauss_image, 30, 120, 3)
    edged_image = cv2.Canny(dilate_image, 30, 120, 3)
    cv2.imwrite("D:/FileData/canny.jpg", edged_image)

    # 找轮廓
    # cnts = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # RETR_EXTERNAL，只检索外框
    cnts = cv2.findContours(edged_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 判断是OpenCV2还是OpenCV3
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # 按轮廓大小降序排列
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    screen_cnt = None

    for c in cnts:
        # 计算轮廓周长
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # 如果我们的近似轮廓有四个点，则确定找到了纸
        if len(approx) == 4:
            screen_cnt = approx
            break

    return screen_cnt, ratio


def test1():
    image = cv2.imread('D:/FileData/1.JPG')
    screen_cnt, ratio = pre_process(image)
    # 对原始图像应用四点透视变换，以获得纸张的俯视图
    warped = four_point_transform(image, screen_cnt.reshape(4, 2) * ratio)

    enhancer = Enhancer()
    enhancedImg = enhancer.gamma(warped, 1.63)

    # 可以根据轮廓大小来判断截取精度
    image_area = enhancedImg.shape[0] * enhancedImg.shape[1]
    if image_area < 250000:
        print('截取不合格')

    cv2.imshow("org", imutils.resize(image, height=500))
    cv2.imshow("gamma", imutils.resize(enhancedImg, height=500))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # 保存
    # cv2.imwrite(filename=os.path.join('./proprecess/2.jpg'), img=enhancedImg)


def test2():

    img = cv2.imread('D:/FileData/11.JPG')

    result1 = img.copy()
    result2 = img.copy()
    result3 = img.copy()

    img = cv2.GaussianBlur(img, (3, 3), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    cv2.imwrite("D:/FileData/canny.jpg", edges)
    # hough transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=90, maxLineGap=10)
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(result1, (x1, y1), (x2, y2), (0, 0, 255), 1)
        print(x1, y1)
        print(x2, y2)
    cv2.circle(result2, (207, 151), 5, (0, 255, 0), 5)
    cv2.circle(result2, (517, 285), 5, (0, 255, 0), 5)
    cv2.circle(result2, (17, 601), 5, (0, 255, 0), 5)
    cv2.circle(result2, (343, 731), 5, (0, 255, 0), 5)

    cv2.imwrite("D:/FileData/result1.jpg", result1)
    cv2.imwrite("D:/FileData/result2.jpg", result2)

    src = np.float32([[207, 151], [517, 285], [17, 601], [343, 731]])
    dst = np.float32([[0, 0], [337, 0], [0, 488], [337, 488]])
    m = cv2.getPerspectiveTransform(src, dst)
    result = cv2.warpPerspective(result3, m, (337, 488))
    cv2.imwrite("D:/FileData/result.jpg", result)
    cv2.imshow("result", result)
    cv2.waitKey(0)


if __name__ == '__main__':
    test1()


