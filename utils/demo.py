#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : demo.py 
# @Software: PyCharm
# @Time : 2019/6/3 8:52


if __name__ == '__main__':
    import re
    # print(re.match('^[0-9]*$', '九'))
    # print(re.match('([一二两三四五六七八九零十百千万亿]+|[0-9])', '草泥马'))

    # 数字
    # print(re.match('[0-9]{1,20}', '12568'))
    # print(re.match('[一二两三四五六七八九十][一二两三四五六七八九零十百千万亿]{0,10}', '两千五百亿'))
    # 金额
    print(re.match('(([一二两三四五六七八九十][一二两三四五六七八九零十百千万亿]{0,10}|[0-9]{1,10})'
                   '[块毛分]){1,3}([一二两三四五六七八九]|[1-9])?', '两千五百块3毛5'))
    # 车牌
    # print(re.match('(京|沪|深|渝|冀|豫|云|辽|黑|湘|皖|鲁)[A-Za-z]\d{3}', '京A573'))

    # import codecs
    #
    # with codecs.open('D:/安装包/词性分析/demo.txt', 'a', encoding='GBK') as f:
    #     f.writelines('^[0-9]{1,20}' + '\n')
    #     f.writelines('^[一二两三四五六七八九十百][一二两三四五六七八九零十百千万亿]{0,20}[一二两三四五六七八九零十百千万亿]' + '\n')

