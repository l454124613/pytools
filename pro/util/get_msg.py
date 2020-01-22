# -*- coding:utf-8 -*-
# Author:lixuecheng

import util.shengshiqu as s
import random
import sys, os
import datetime

ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase


def get_FileModifyTime(filePath):
    filePath = filePath.replace('"', '')
    t = os.path.getmtime(filePath)
    return t


def get_address_cn():
    return s.get_random_city()['str']


def get_function_name():
    return sys._getframe().f_back.f_back.f_code.co_name


def get_random_int(n=4):
    n1 = 1
    n = abs(int(n))
    for _ in range(n):
        n1 *= 10
    return random.randint(1, n1)


def get_random_ssn(min_age=18, max_age=90):
    def checksum(s):
        return str((1 - 2 * int(s, 13)) % 11).replace('10', 'X')

    diqu = s.get_random_city()['county_code']
    age = datetime.timedelta(days=random.randint(
        min_age * 365, max_age * 365))
    birthday = datetime.date.today() - age
    birthday_str = birthday.strftime('%Y%m%d')
    ssn_without_checksum = diqu + birthday_str + str(get_random_int(3))
    return ssn_without_checksum + checksum(ssn_without_checksum)


def get_random_element(n=4,key='ul'):
    '''
    n 为数量
    key u大写 l小写 ul可以连用
    '''
    n1 = ''
    n = abs(int(n))
    v=''
    if 'U' in key.upper():
        v=ascii_uppercase
    if 'L' in key.upper():
        v+=ascii_lowercase
    for _ in range(n):
        n1 += random.choice(v)
    return n1


def get_random_int_element(n=4):
    n1 = ''
    n = abs(int(n))
    for _ in range(n):
        if random.choice([True, False]):
            n1 += get_random_element(1)
        else:
            n1 += str(random.randint(0, 9))
    return n1

