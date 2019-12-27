# -*- coding:utf-8 -*-
# Author:lixuecheng

import time
import datetime
from dateutil.relativedelta import relativedelta
import urllib.parse as p
import json
import re


def p_to_uri(ss):
    return p.quote(ss)


def p_to_None_value(guding, val):
    if val is None:
        return ''
    else:
        return guding + str(val)


def p_from_uri(ss):
    return p.unquote(ss)


def p_get_data_re(da):
    return re.findall(r"\$\{(.+?)\}", da)


# 转换格式，把 a:b;c:d转换成对应的dict形式，返回的key需要去头4位
def p_str2split(ss, sp=';', re='dic'):
    pa2 = ss.replace('\n', '').replace('\r', '').replace('  ', ' ').replace('，', ',').replace('；', ';').split(sp)
    if re == 'dic':
        dd = {}
    else:
        dd = []
    n = 1000
    for i in pa2:
        i = i.replace('：', ':')
        if len(i.strip()) > 0 and ':' in i:
            n += 1
            tmp = i.split(':')
            if re == 'dic':
                dd[str(n) + tmp[0]] = i.replace(tmp[0] + ':', '')
            else:
                dd.append({tmp[0], i.replace(tmp[0] + ':', '')})
    return dd


def p_addhttp(ss):
    if ss.lower().replace('：', ':').startswith('http://'):
        return ss
    elif ss.lower().replace('：', ':').startswith('https://'):
        # raise Exception('暂时不支持https的请求')
        return ss
    else:
        return 'http://' + ss


def p_str2content_type(ss):
    if ss is None or ss == '':
        return "application/json;charset=UTF-8"
    elif ss.lower() == 'json':
        return "application/json;charset=UTF-8"
    elif ss.lower() == 'text':
        return "text/plain;charset=UTF-8"
    elif ss.lower() == 'form':
        return "application/x-www-form-urlencoded"
    elif ss.lower() == 'multipart':
        return False
    else:
        return ss


def p_obj2json(ss, ccc=None):
    if isinstance(ss, str):
        return ss
    else:
        if ccc is None:
            return json.dumps(ss, ensure_ascii=False)
        else:
            return json.dumps(ss, ensure_ascii=False, cls=ccc)


def p_json2obj(ss):
    if isinstance(ss, str):
        return json.loads(ss)
    elif isinstance(ss, dict) or isinstance(ss, list):
        return ss
    else:
        raise Exception('请输入规则的字符串')


def p_get_now_time(ss="%H:%M:%S"):
    return time.strftime(ss)


def p_get_now_date(ss="%Y-%m-%d"):
    return time.strftime(ss)


def p_form2time(t, f):
    try:
        tt = time.strptime(t, f)
    except Exception as e:
        print(e, '输入:', t, '错误，先默认今天')
        return int(time.time())
    return int(time.mktime(tt))


def time2form(t):
    a = int(t)
    if a >= 153654799100:
        a = a / 1000
    return time.strftime('%Y-%m-%d', time.localtime(a))


def p_get_month_fristday(d=0, m=0, y=0, t=None, f=None):
    if t is None:
        t = datetime.date.today()
    else:
        t = datetime.date.fromtimestamp(p_form2time(re.sub(r'\D', '', t)[:8], '%Y%m%d'))
    t2 = datetime.date(t.year, t.month, 1) - relativedelta(years=y) - relativedelta(months=m) - datetime.timedelta(
        days=d)
    if f is None:
        return str(t2)
    else:
        return str(t2.strftime(f))


def p_get_month_lastday(d=0, m=0, y=0, t=None, f=None):
    if t is None:
        t = datetime.date.today()
    else:
        t = datetime.date.fromtimestamp(p_form2time(re.sub(r'\D', '', t)[:8], '%Y%m%d'))
    t2 = datetime.date(t.year, t.month, 1) - relativedelta(years=y) - relativedelta(
        months=(m - 1)) - datetime.timedelta(
        days=1) - datetime.timedelta(
        days=d)
    if f is None:
        return str(t2)
    else:
        return str(t2.strftime(f))


def p_get_fix(d=0, m=0, y=0, t=None, f=None):
    if t is None:
        t = datetime.date.today()
    else:
        t = datetime.date.fromtimestamp(p_form2time(re.sub(r'\D', '', t)[:8], '%Y%m%d'))
    t2 = t - relativedelta(years=y) - relativedelta(months=m) - datetime.timedelta(
        days=d)
    if f is None:
        return str(t2)
    else:
        return str(t2.strftime(f))
