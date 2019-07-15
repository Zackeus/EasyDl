#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : demo.py 
# @Software: PyCharm
# @Time : 2019/6/3 8:52


import time
from utils import MyThread


def test(i):
    print(i, 'start')
    if i == 3:
        time.sleep(30)
    time.sleep(i * 5)
    print(i, 'end')


if __name__ == '__main__':

    # 线程组
    threads = []

    for ti in [0, 1, 2, 3]:
        t = MyThread(target=test, args=(ti, ))
        threads.append(t)

    for i in range(len(threads)):
        threads[i].setDaemon(True)
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join(13)
        if threads[i].exception:
            raise threads[i].exception


