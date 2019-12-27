# -*- coding:utf-8 -*-
# Author:lixuecheng
def check_none(*val):
    num = 0
    for i in val:
        if i is None:
            num += 1
    return num





def check_none_kong(*val, is_strip=True):
    num = 0
    if is_strip:
        for i in val:
            if i is None or (isinstance(i, str) and i.strip() == ''):
                num += 1
    else:
        for i in val:
            if i is None or i == '':
                num += 1
    return num
