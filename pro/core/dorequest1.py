# -*- coding:utf-8 -*-
# Author:lixuecheng

import time

from requests import session

import pro.config.sys_config as conf
from pro.core.baseClass import base_class
from pro.dom.report import TestReport
from pro.dom.request_dom import (
    add2global2, check_res, log, logger, other_action, other_action_step,
    request_prepare)
from pro.util.parse_msg import p_addhttp, p_to_None_value, p_to_uri

'''生成报告'''
rep = TestReport()


'''
da 用例数据：
    status 是否运行 run 为运行
    forward 是前置用例，可以支持多个，但只测过一个
    casename 用例名称
    总的参数：
    {'sheetname': 表格名称，选填, 'casename':用例名称，名称有唯一性，必填 , 'method': 请求方法，必填, 'ip': 请求ip和端口，必填,
         'path': 请求路径必填, 'da': 请求体，选填, 'header':请求头信息，选择 , 'pa': 参数，必填, 'forward': 前置用例，选填,
        'pre': 前置操作，选填, 're': 后置操作，选填, 'cvalue': 值校验，必填, 'csql': 数据库校验，选填,
         'row_num': 记录行号，选填}
gg 全局变量
f 输入的参数值

'''
@log
def run_case(da, gg, f=None):
    isrun = False  # 检查当前用例是否需要执行，当状态为执行时，会执行；当用户为前置用例时，会执行
    if da['status'] == 'run':
        rep.clear_res()

        isrun = True
    if f is not None:
        isrun = True

    if da['forward'] is None:
        # 没有前置用例
        if isrun:
            # 执行用例
            a, b = DoRequest(da, gg).request(f)
            if not a:
                # 失败，记录失败日志
                rep.add_res(da['casename'], 2, str(b))

                return False, da['casename'] + '执行出现错误:' + str(b)
            else:
                # 成功，记录成功日志
                rep.add_res(da['casename'], 1)
                return True, ''
        else:
            return False, da['casename'] + '作为基础方法等待调用'

    else:
        if isrun:
            # 有前置用例
            names = da['forward'].strip().replace(
                '；', ';').split(';')  # 列出前置用例
            for name1 in names:
                name1 = name1.replace(' ', '').replace('\r', '').replace('\n', ''). \
                    replace(r'\r', '').replace(
                        r'\n', '').replace('：', ':')  # 去除空格换行等符号
                if name1.startswith('//') or name1.startswith('#'):  # 去除注释
                    continue
                n1 = name1.split(':')  # 区分用例名称和参数
                if len(n1) == 2:
                    # 获取前置用例的请求参数值
                    ca = gg['cases'].get(n1[0])
                    if ca is None:
                        rep.add_res(da['casename'], 0, '找不到前置用例:' + n1[0])

                        return False, '找不到前置用例:' + n1[0]
                    else:
                        # 运行前置用例
                        r1 = run_case(ca, gg, n1[1])
                else:
                    # 无前置用例数据，导致当前用例无法执行，记录日志
                    rep.add_res(da.get('casename'), 0,
                                '前置用例格式不正确，' + name1)
                    return False, '前置用例格式不正确，' + name1
                if r1[0]:
                    # 前置用例执行后，运行当前用例
                    a, b = DoRequest(da, gg).request()
                    if not a:
                        # 记录错误记录
                        rep.add_res(da['casename'], 2, str(b))

                        return False, da['casename'] + '执行出现错误:' + str(b)
                        # raise Exception()
                    else:
                        # 正确记录
                        rep.add_res(da['casename'], 1)
                        return True, ''
                else:
                     # 前置用例数据执行错误，导致当前用例无法执行，记录日志
                    rep.add_res(da['casename'], 0, '由于前置用例：' +
                                ca['casename'] + '，执行失败，当前用例无法执行' + str(r1[1]))
                    return False, '由于前置用例：' + ca['casename'] + '，执行失败，当前用例无法执行' + str(r1[1])
        else:
            return False, da['casename'] + '作为基础方法等待调用'


@log
def run_case_step(da, gg, f=None):
    isrun = False
    if da['status'] == 'run':
        rep.clear_res()

        isrun = True
    if f is not None:
        isrun = True

    if da['forward'] is None:
        # if forward == '':
        if isrun:
            kkey = DoRequest(da, gg, is_step=True).request_step(f)
            while True:

                try:
                    a, b = next(kkey)
                    if a == 'err':
                        print(da['casename'], a, b)
                        rep.add_res(da['casename'], 2, str(b))
                        yield False, da['casename'] + '执行出现错误:' + str(b)
                    elif a == 'para':
                        yield a, b
                        pass
                    elif a == 'end':
                        if b == 'ok':
                            print(da['casename'], a)
                            rep.add_res(da['casename'], 1)
                            yield True, ''
                    else:
                        yield a, b

                except StopIteration:
                    break

        else:
            print(da['casename'] + '作为基础方法等待调用')
            yield False, da['casename'] + '作为基础方法等待调用'

    else:

        names = da['forward'].strip().replace('；', ';').split(';')
        for name in names:
            name = name.replace(' ', '').replace('\r', '').replace('\n', '').replace(r'\r', '').replace(r'\n',
                                                                                                        '').replace(
                '：',
                ':')
            if name.startswith('//'):
                continue
            n1 = name.split(':')
            if len(n1) == 2:
                ca = gg['cases'].get(n1[0])
                if ca is None:
                    rep.add_res(da['casename'], 0, '找不到前置用例:' + n1[0])
                    yield False, '找不到前置用例:' + n1[0]

                else:
                    r1 = True
                    keyr1 = run_case_step(ca, gg, n1[1])
                    while True:
                        try:
                            a, b = next(keyr1)
                            if a:
                                if b == '':
                                    pass
                                    # r1 = True

                                else:
                                    yield a, b
                            else:
                                r1 = False
                                yield a, b

                        except StopIteration:
                            break

            else:
                rep.add_res(da['casename'], 0, '前置用例格式不正确，' + name)
                yield False, '前置用例格式不正确，' + name
                # return False, '前置用例格式不正确，' + name
                # raise Exception('前置用例格式不正确，' + name)
            if r1:
                kkey = DoRequest(da, gg, is_step=True).request_step(f)
                while True:

                    try:
                        a, b = next(kkey)
                        if a == 'err':
                            print(da['casename'], a, b)
                            rep.add_res(da['casename'], 2, str(b))
                            yield False, da['casename'] + '执行出现错误:' + str(b)
                        elif a == 'para':
                            yield a, b
                            pass
                        elif a == 'end':
                            if b == 'ok':
                                print(da['casename'], a)
                                rep.add_res(da['casename'], 1)
                                yield True, ''
                        else:
                            yield a, b

                    except StopIteration:
                        break

            else:

                rep.add_res(da['casename'], 0, '由于前置用例：' +
                            ca['casename'] + '，执行失败，当前用例无法执行')
                yield False, '由于前置用例：' + ca['casename'] + '，执行失败，当前用例无法执行'


def get_report(_path=None):
    return rep.create_report(_path)


class DoRequest:
    @log
    def __init__(self, da, gg, px=None, is_step=False):
        # {'sheetname': str(i), 'casename': name, 'method': method, 'ip': ip,
        #  'path': path, 'da': da, 'header': header, 'pa': pa, 'forward': forward,
        #  'pre': preaction, 're': reaction, 'cvalue': cvalue, 'csql': csql,
        #  'row_num': j}
        if px is not None:
            # global2['proxies'] = {"http": p_addhttp(px), "https": p_addhttp(px)}
            self.proxies = {"http": p_addhttp(px), "https": p_addhttp(px)}
        else:
            self.proxies = None
            # global2['proxies'] = None

        self.s = session()
        self.s.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537' \
                            '.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
        self.string = p_to_None_value('name=', da.get('casename')) + ',url=' + da['ip'] + da['path'] + ',method=' + da[
            'method'] + p_to_None_value(',header=', da.get('header'))
        self.gg = gg
        self.dic = gg.copy()
        # 初始化方法
        self.dic[conf.add_header] = _AddHeader(self.s)
        self.dic[conf.wait_second] = _Wait()
        self.dic[conf.kong] = None
        self.dic[conf.get_res] = _Addres()

        # 初始化请求

        self.req = {'method': da['method'], 'ip': da['ip'],
                    'path': da['path'], 'da': da['da'], 'header': da['header']}
        self.pre = da['pre']
        self.re = da['re']
        self.check = check_res(da['cvalue'], da['csql'], gg, is_step)
        self.info = {'sheetname': da.get('sheetname'), 'casename': da.get(
            'casename'), 'row_num': da.get('row_num')}
        self.pa = da['pa']

    def __str__(self):
        try:
            return 'request_' + self.string
        except:
            return 'request'

    @log
    def request(self, para=None):
        # 输入参数
        try:
            if para is None:
                add2global2(self.pa, self.dic)
            else:
                para = para.replace(' ', '').replace('\n', '').replace('\r', '') \
                    .replace(r'\n', '').replace(r'\r', '').replace('，', ',')
                pa = self.pa.replace(' ', '').replace('\n', '').replace('\r', '') \
                    .replace(r'\n', '').replace(r'\r', '').replace('，', ','). \
                    replace('；', ';').replace('：', ':')
                p1 = para.strip(',').split(',')
                p2 = pa.strip(';').split(';')
                d = {}
                if len(p1) == len(p2):
                    for i in range(len(p1)):
                        i1 = p2[i].split(':')
                        if len(i1) == 2:
                            d[i1[0]] = p1[i]

                        else:
                            # return False, '方法的参数格式不正确' + i
                            raise Exception('方法的参数格式不正确' + str(i))
                    add2global2(d, self.dic)

                else:
                    raise Exception('方法参数和实际输入参数不一致，' + para + '期望：' + pa)

            # 进行前置操作
            other_action(self.pre, str(self.info['casename']), self.dic)

            # 准备请求
            req = request_prepare(self.req['method'], self.req['ip'], self.req['path'], self.req['da'],
                                  self.req['header'], self.dic)
            if req['header_content_type'] is not None:
                self.s.headers['Content-Type'] = req['header_content_type']
            logger.info('请求链接：' + req['ip'] + req['path'])
            logger.info('请求头信息：' + str(self.s.headers))
            if self.proxies is not None:
                logger.info('请求代理：' + str(self.proxies))

            if req['data'] is not None:
                logger.info('请求数据：' + str(req['data']))

            # 发起请求
            self.res = None
            res = self.s.request(
                req['method'], req['ip'] + req['path'], proxies=self.proxies, data=req['data'])
            res.encoding = 'utf-8'

            self.check(res)
            self.res = res
            self.res_b = True
            self.e = ''

        except Exception as e:

            logger.error(self.info['casename'] + '运行失败,' + str(e))
            self.res_b = False
            self.e = str(e)

        finally:
            try:
                other_action(self.re, str(
                    self.info['casename']), self.gg, True, self.res)
            except:
                pass
            logger.info('##############################%s############################' % str(
                self.info['casename']))
            return self.res_b, self.e

    @log
    def request_step(self, para=None):

        # 输入参数
        try:
            if para is None:
                add2global2(self.pa, self.dic)
            else:
                para = para.replace(' ', '').replace('\n', '').replace('\r', '') \
                    .replace(r'\n', '').replace(r'\r', '').replace('，', ',')
                pa = self.pa.replace(' ', '').replace('\n', '').replace('\r', '') \
                    .replace(r'\n', '').replace(r'\r', '').replace('，', ','). \
                    replace('；', ';').replace('：', ':')
                p1 = para.strip(',').split(',')
                p2 = pa.strip(';').split(';')
                d = {}
                if len(p1) == len(p2):
                    for i in range(len(p1)):
                        i1 = p2[i].split(':')
                        if len(i1) == 2:
                            d[i1[0]] = p1[i]

                        else:
                            raise Exception('方法的参数格式不正确' + str(i))
                    add2global2(d, self.dic)

                else:
                    raise Exception('方法参数和实际输入参数不一致，' + para + '期望：' + pa)

            on1 = other_action_step(self.pre, self.info['casename'], self.dic)
            while True:
                try:
                    a, b = next(on1)
                    if not a:
                        yield a, b
                        return
                    else:
                        yield a, b
                except StopIteration:
                    break
            yield 'para', 'ok'
            inter_info = ''
            self.res = None
            req = request_prepare(self.req['method'], self.req['ip'], self.req['path'], self.req['da'],
                                  self.req['header'], self.dic)
            if req['header_content_type'] is not None:
                self.s.headers['Content-Type'] = req['header_content_type']
            logger.info('请求链接：' + req['ip'] + req['path'])
            logger.info('请求头信息：' + str(self.s.headers))
            inter_info += '请求链接：' + req['ip'] + req['path'] + p_to_uri('<br>')
            inter_info += '请求头信息：' + str(self.s.headers)
            if self.proxies is not None:
                logger.info('请求代理：' + str(self.proxies))
                inter_info += '请求代理：' + p_to_uri(str(self.proxies))

            if req['data'] is not None:
                logger.info('请求数据：' + str(req['data'].decode('utf-8')))
                inter_info += '<br>' + '请求数据：' + p_to_uri(str(req['data'].decode('utf-8').replace(
                    '\r', '').replace('\n', '<br>').replace('\t', ' ')))
            yield 'inter', inter_info
            res = self.s.request(
                req['method'], req['ip'] + req['path'], proxies=self.proxies, data=req['data'])
            res.encoding = 'utf-8'
            yield 'inter', p_to_uri(str(res.status_code) + '<br>' + str(res.headers) + '<br>' + res.text.replace(
                '\r', '').replace('\n', '<br>').replace(
                '\t', ' '))
            yield 'para', 'ok'

            on2 = self.check(res)
            while True:
                try:
                    yield next(on2)
                except StopIteration:
                    break
            yield 'para', 'ok'
            self.res = res
            self.res_b = 'ok'
            self.e = ''

        except Exception as e:
            # print(self.info['casename'] + '运行失败')
            self.e = e
            self.res_b = 'no'

            yield 'err', str(e)

            logger.error(self.info['casename'] + '运行失败,' + str(e))

        finally:
            try:
                on3 = other_action_step(
                    self.re, self.info['casename'], self.gg, True, self.res)
                while True:
                    try:
                        yield next(on3)
                    except StopIteration:
                        break
                yield 'para', 'ok'
            except:
                pass
            yield 'end', self.res_b
            logger.info('##############################%s############################' % str(
                self.info['casename']))


class _AddHeader(base_class):
    def __init__(self, s):
        self.s = s
        self.string = '添加请求头'

    @log
    def run(self, dd, name, gg, isafter=False):
        vak = dd.replace('，', ',').split(',')
        self.s.headers[vak[0]] = vak[1]
        self.string = name + ',添加请求头，key:%s ,value:%s' % (vak[0], vak[1])
        logger.info(name + ',添加请求头，key:%s ,value:%s' % (vak[0], vak[1]))

    def __str__(self):
        try:
            return self.string
        except:
            return '添加请求头'


class _Addres(base_class):
    def __init__(self):
        self.string = '提取结果值'

    '''
    dd 提取信息 ?=[]/?=s.12.cd
    res 请求结果
    gg 全局变量
    '''

    @log
    def run(self, dd, res, gg, isheader=False):
        d1 = dd.replace('【', '[').replace('】', ']').split('=')
        re = ''
        if len(d1) == 2:
            if d1[1].strip().startswith('['):
                if d1[1].strip().replace(' ', '') == '[]':
                    if not isheader:
                        re = res.text
                    else:
                        re = str(res.headers)
                    add2global2({d1[0]: re}, gg)
                else:
                    d2 = d1[1].replace(' ', '').replace(
                        '，', ':').replace(',', ':')
                    if not isheader:
                        re = eval('res.text' + d2)
                    else:
                        re = eval('str(res.headers)' + d2)
                    add2global2({d1[0]: re}, gg)
            else:
                d2 = d1[1].split('.')
                try:
                    if not isheader:
                        re = res.json()
                    else:
                        re = res.headers
                    for i in d2:
                        if i.isdigit():
                            re = re[int(i)]
                        else:
                            re = re[i]

                except:
                    raise Exception('提取结果失败，请校验格式：' + d1 + ',结果：' + re)
                add2global2({d1[0]: re}, gg)

        else:
            raise Exception('提取结果格式错误：' + dd)

        self.string = '提取结果，key:%s ,value:%s' % (d1[1], re)
        return '提取结果，key:%s ,value:%s' % (d1[1], re)
        # logger.info(name + ',添加请求头，key:%s ,value:%s' % (vak[0], vak[1]))

    def __str__(self):
        try:
            return self.string
        except:
            return '提取结果值'


class _Wait(base_class):
    def __init__(self):

        self.string = '等待'

    @log
    def run(self, dd, name2, gg, isafter=False):
        n = int(dd)
        time.sleep(n)

        self.string = name2 + ',等待%d秒' % n
        logger.info(name2 + ',等待%d秒' % n)

    @log
    def check(self, dd, name1):
        n = int(dd)
        time.sleep(n)
        self.string = name1 + ',等待%d秒' % n
        logger.info(name1 + ',等待%d秒' % n)

    def __str__(self):
        try:
            return self.string
        except:
            return '等待'
