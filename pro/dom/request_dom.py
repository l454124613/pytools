# -*- coding:utf-8 -*-
# Author:lixuecheng
from util.parse_msg import p_get_data_re, p_str2split, p_str2content_type, p_addhttp, p_obj2json, p_json2obj
from urllib3 import encode_multipart_formdata
from core.logger import log, logger, global2
from util.get_msg import *
from util.parse_msg import *


@log
def request_prepare(method, ip, path, da, header, gg):
    ip = p_addhttp(_check_para(ip, gg))  # 参数字填充，校验http
    path = _check_para(path, gg)  # 路径参数填充
    da = _check_para(da, gg)  # 固定参数填充
    if da is None or da == '':
        da = None
    try:
        header = p_str2content_type(header)  # 请求头类型匹配
    except:
        pass
    # 遇到multipart请求的处理
    if isinstance(header, bool) and not header:
        da = p_json2obj(da)
        if 'file' in da:
            if not os.path.exists(da['file']):
                raise Exception(da['file'] + ',文件不存在')
            else:
                file = da['file']
            da['file'] = (os.path.basename(file), open(file, 'rb').read())
        encode_data = encode_multipart_formdata(da)
        header = encode_data[1]
        da = encode_data[0]
        return {'method': method, 'ip': ip, 'path': path, 'data': da,
                'header_content_type': header}
    else:
        return {'method': method, 'ip': ip, 'path': path, 'data': da.encode('utf8'),
                'header_content_type': header}


# logger.debug({'method': method, 'ip': ip, 'port': port, 'path': path, 'data': da,
#               'header_content_type': header})


@log
def add2global2(pa, gg):
    if isinstance(pa, dict):
        gg.update(pa)
    elif isinstance(pa, str):
        if pa.replace('：', ':').find(':') != -1:
            # pa = _check_para(pa)
            dd = p_str2split(pa)
            for i, j in dd.items():
                # i = i[4:]
                # if global2['运行要求'] == '流程' and i.startswith('//'):
                #     continue
                # else:
                gg[i[4:]] = j
            # global2.update(dd)
        else:
            raise Exception(pa + ',输入格式错误1，请查看')
    elif pa is None:
        pass
    else:
        raise Exception(pa + ',输入格式错误2，请查看')


# @log
# def other_step_action(ss, name, isafter=False):
#     if ss is None:
#         return '没有前置的内容'
#     ac = p_str2split(ss, ';', re='lis')
#     tva = set()
#     ll = len(ac)
#
#     def next():
#         if ll == 0:
#             if isafter:
#                 return '后置执行完成'
#             else:
#                 return '前置执行完成'
#         else:
#             ll -= 1
# class other_step_action:
#     def __init__(self, ss, name, isafter=False, ischeck=False):
#         self.ss = ss
#         self.name = name
#         self.isafter = isafter
#         self.ischeck = ischeck
#         self.tva = set()
#         self.status = 0
#         self.run_line = 0
#         self.ac = None
#         self.va = None
#         self.re = None
#         self.ll = 0
#
#     def anal(self):
#         if self.ss is None:
#             if self.ischeck:
#                 return '没有校验的内容'
#             if self.isafter:
#                 return '没有后置的内容'
#             else:
#                 return '没有前置的内容'
#         self.ac = p_str2split(self.ss, ';', re='lis')
#         self.ll = len(self.ac)
#         if self.ll == 0:
#             self.status = 4
#         else:
#             self.status = 1
#
#     def look(self):
#         # s1 = ''
#         if self.status == 4:
#             if self.ischeck:
#                 return '校验值已无后续执行'
#             if self.isafter:
#                 return '后置已无后续执行'
#             else:
#                 return '前置已无后续执行'
#         elif self.status == 1:
#             di = self.ac[self.run_line]
#             for i, j in di.items():
#                 if i.startswith('//') or j.startswith('//'):
#                     self.status = 2
#                     self.run_line += 1
#                     return i + ':' + j + ',跳过运行'
#                 else:
#                     if global2.get(i) is not None:
#
#                         va = global2.get(i)
#
#                         re = _check_para(j)
#                         self.va = va
#                         self.re = re
#                         self.status = 6
#                         # va.run(re, name, isafter)
#                         # tva.add(va)
#                         return '执行' + i + ':' + re
#
#                     else:
#                         raise Exception(i + '无此方法，请查询')
#         elif self.status == 5:
#             return '提交所有的执行结果'
#
#     def run(self):
#         if self.status == 4:
#             if self.ischeck:
#                 return '校验值已无后续执行'
#             if self.isafter:
#                 return '后置已无后续执行'
#             else:
#                 return '前置已无后续执行'
#         elif self.status == 2:
#             self.status = 3
#             return '跳过'
#         elif self.status == 5:
#             for i in self.tva:
#                 i.commit()
#             self.status = 4
#             return '执行成功'
#             pass
#         else:
#             try:
#                 if self.ischeck:
#                     re = self.va.check(self.re)
#                 else:
#                     re = self.va.run(self.re, self.name, self.isafter)
#             except Exception as e:
#                 for i in self.tva:
#                     i.rollback()
#                     self.status = 4
#                 return '执行失败,已回滚：' + str(e)
#             self.run_line += 1
#             if self.run_line == self.ll:
#                 for i in self.tva:
#                     i.commit()
#
#                 self.status = 4
#             else:
#                 self.status = 3
#
#             if len(re) == 2:
#                 return 'mysql结果：影响行数：%s,结果：%s' % (str(re[0]), str(re[1]))
#             else:
#                 return str(re)


@log
def other_action_step(ss, name, gg, isafter=False, res=None):
    if ss is None or ss.strip() == '':
        return
    ac = p_str2split(ss, ';')
    tva = set()
    try:
        for i, j in ac.items():
            i = i[4:].strip()
            if i.startswith('//') or j.startswith('//'):
                continue
            # if global2['运行要求'] == '流程':
            #     if i.startswith('//') or j.startswith('//'):
            #         continue
            # else:
            #     i = i.replace('//', '')
            #     j = j.replace('//', '')
            if gg.get(i) is not None:

                va = gg.get(i)

                re = _check_para(j, gg)
                yield i, re
                if isafter and res is not None:
                    # 提取结果值使用

                    va.run(re, res, gg, isafter)

                else:

                    va.run(re, name, gg, isafter)

                tva.add(va)



            else:
                # yield False, i + '无此方法，请查询'
                # return ''
                raise Exception(i + '无此方法，请查询,' + str(j))
        for i in tva:
            i.commit()
        if not isafter:
            print(name + '前置已运行' + str(len(tva)) + '条')
            logger.info(name + '前置已运行' + str(len(tva)) + '条')
        else:
            print(name + '后置已运行' + str(len(tva)) + '条')
            logger.info(name + '后置已运行' + str(len(tva)) + '条')
    except Exception as e:
        for i in tva:
            i.rollback()
        if not isafter:
            # print(name + '前置运行失败')
            logger.warn(name + '前置运行失败')
        else:
            # print(name + '后置运行失败')
            logger.warn(name + '后置运行失败')

        yield False, '执行失败，' + str(e)

        # raise e

    return


@log
def other_action(ss, name, gg, isafter=False, res=None):
    if ss is None:
        return 'no'
    ac = p_str2split(ss, ';')
    tva = set()
    try:
        for i, j in ac.items():
            i = i[4:].strip()
            if i.startswith('//') or j.startswith('//'):
                continue
            # if global2['运行要求'] == '流程':
            #     if i.startswith('//') or j.startswith('//'):
            #         continue
            # else:
            #     i = i.replace('//', '')
            #     j = j.replace('//', '')
            if gg.get(i) is not None:

                va = gg.get(i)

                re = _check_para(j, gg)
                # yield i, re
                if isafter and res is not None:
                    # 提取结果值使用
                    va.run(re, res, gg, isafter)
                else:

                    va.run(re, name, gg, isafter)
                tva.add(va)



            else:
                raise Exception(i + '无此方法，请查询')
        for i in tva:
            i.commit()
        if not isafter:
            print(name + '前置已运行' + str(len(tva)))
            logger.info(name + '前置已运行' + str(len(tva)))
        else:
            print(name + '后置已运行' + str(len(tva)))
            logger.info(name + '后置已运行' + str(len(tva)))
    except Exception as e:
        for i in tva:
            i.rollback()
        if not isafter:
            # print(name + '前置运行失败')
            logger.warn(name + '前置运行失败')
        else:
            # print(name + '后置运行失败')
            logger.warn(name + '后置运行失败')

        raise e

    return 'ok'


class check_step_res:
    def __init__(self, cval):
        cv = str(cval)
        tl = []
        cv2 = cv.replace('\n', '').replace('\r', '').replace('  ', ' ').replace('，', ',').replace('；', ';').replace('：',
                                                                                                                    ':').split(
            ';')
        for i in cv2:
            dd = {}
            if i.startswith('~'):
                dd['ctype'] = 'contain'
                dd['value'] = i[1:]
            elif i.startswith('!'):
                dd['ctype'] = 'not'
                dd['value'] = i[1:]
            elif i.lower() == 'true' or i.lower() == 'false':
                dd['ctype'] = 'bool'
                dd['value'] = i
            elif i.find(':') != -1:
                dd['ctype'] = 'json'
                dd['value'] = i
            else:
                if i.isdigit():
                    i1 = int(i)
                    if i1 > 99 and i1 < 600:
                        dd['ctype'] = 'status'
                        dd['value'] = i
                    else:
                        dd['ctype'] = 'match'
                        dd['value'] = i
                else:
                    if len(i) > 0:
                        dd['ctype'] = 'match'
                        dd['value'] = i
                    else:
                        logger.warn(i + ',没有找到对应校验方法')
            tl.append(dd)
        self.t = tl


@log
def check_res(cval, csql, gg, is_step=False):
    cv = str(cval)
    # td = p_str2split(cv, ';')
    tl = []

    cv2 = cv.replace('\n', '').replace('\r', '').replace('  ', ' ').replace('，', ',').replace('；', ';').replace('：',
                                                                                                                ':').split(
        ';')
    for i in cv2:
        dd = {}
        if i.startswith('~'):
            dd['ctype'] = 'contain'
            dd['value'] = i[1:]
        elif i.startswith('!'):
            dd['ctype'] = 'not'
            dd['value'] = i[1:]
        elif i.lower() == 'true' or i.lower() == 'false':
            dd['ctype'] = 'bool'
            dd['value'] = i
        elif i.find(':') != -1:
            dd['ctype'] = 'json'
            dd['value'] = i
        else:
            if i.isdigit():
                dd['ctype'] = 'status'
                dd['value'] = i
            else:
                if len(i) > 0:
                    dd['ctype'] = 'match'
                    dd['value'] = i
                else:
                    logger.warn(i + ',没有找到对应校验方法')

        tl.append(dd)

    def check_step(r, **kwargs):
        # try:
        #     # logger.info('响应状态码:' + str(r.status_code))
        #     # logger.info('响应头信息：' + str(r.headers))
        #     # logger.info('响应数据：' + r.text)
        # except:
        #     pass

        # print(kwargs)
        for dd in tl:
            cv = dd['value']
            if dd['ctype'] == 'json':
                if str(r.status_code).startswith('20') and 'Content-Type' in r.headers and r.headers[
                    'Content-Type'].startswith('application/json'):
                    vak = cv.split(':')
                    ke = vak[0].split('.')
                    re = r.json()
                    for i in ke:
                        if i.isdigit():
                            if len(re) > int(i):
                                re = re[int(i)]
                            else:
                                raise Exception('校验结果时，无法提取字段：' + vak[0])
                        else:
                            if not isinstance(re, dict) or re.get(i) is None:
                                raise Exception('校验结果时，无法提取字段：' + vak[0])
                            else:
                                re = str(re[i])
                    # if str(vak[1]).lower()=='true':
                    #     if not isinstance(re,str) and len(re)>0

                    if isinstance(re, str):
                        yield 'json:' + cv, str(vak[1]).strip()

                        if str(re).strip() != str(vak[1]).strip():
                            raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % (str(vak[1]), str(re)))
                        else:
                            logger.info(cv + '，数据校验成功')
                    else:
                        yield 'json:' + cv, str(len(re))
                        if str(vak[1]).lower() == 'true':
                            if len(re) > 0:
                                logger.info(cv + '，数据校验成功')
                            else:
                                raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % ('存在数据', '没有数据'))
                        elif str(vak[1]).lower() == 'false':
                            if len(re) == 0:
                                logger.info(cv + '，数据校验成功')
                            else:
                                raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % ('不存在数据', '有数据'))
                        else:
                            raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % (str(vak[1]), str(re)))
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是键值对：' + cv)
            elif dd['ctype'] == 'contain':
                yield 'contain:' + cv, r.text
                if str(r.status_code).startswith('20') and len(r.text) > 0:
                    if r.text.find(cv) == -1:
                        raise Exception('响应结果不包含：' + cv)
                    else:
                        logger.info(cv + '存在，数据校验成功')
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是含有：' + cv)
            elif dd['ctype'] == 'match':
                yield 'match:' + cv, r.text
                if str(r.status_code).startswith('20') and len(r.text) > 0:
                    if r.text != cv:
                        raise Exception('响应结果不完全匹配：' + cv)
                    else:
                        logger.info(cv + '，数据校验成功')
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是匹配：' + cv)
            elif dd['ctype'] == 'status':
                yield 'status_code:' + str(cv), str(r.status_code)
                if str(r.status_code) != str(cv):
                    raise Exception('接口响应代码不正确，为' + str(r.status_code) + '，期望：' + str(cv))
                else:
                    logger.info(cv + '状态码匹配，数据校验成功')
            elif dd['ctype'] == 'bool':
                yield '是否有值:' + cv, str(len(r.text))
                if str(r.status_code).startswith('20'):
                    is_ok = True
                    ress = '有'
                    if cv.lower() != 'true':
                        is_ok = False
                        ress = '无'
                    if is_ok == len(r.text) > 0:
                        logger.info('结果数据%s，校验成功' % ress)
                    else:
                        raise Exception('结果数据%s，校验失败，结果：%s' % (ress, r.text))
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text)
            elif dd['ctype'] == 'not':
                yield 'not_contain:' + cv, r.text
                if str(r.status_code).startswith('20') and len(r.text) > 0:
                    if r.text.find(cv) == -1:
                        logger.info(cv + '不匹配，数据校验成功')
                    else:

                        raise Exception('响应结果不包含：' + cv)
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是含有：' + cv)
        # yield 'para', 'ok'
        tva = set()
        if csql is not None:
            ac = p_str2split(csql, ';')
            try:
                for i, j in ac.items():
                    i = i.split('_')[1]
                    if gg.get(i) is not None:
                        va = gg.get(i)

                        vv1 = _check_para(j, gg)
                        yield i, vv1
                        va.check(vv1)
                        tva.add(va)
                        # va.commit()
                    else:
                        raise Exception(i + '无此方法，请查询')
                for i in tva:
                    i.commit()
            except Exception as e:
                for i in tva:
                    i.rollback()
                raise Exception('运行sql校验失败,' + str(e))

        # return r

    def check(r, **kwargs):
        # try:
        #     # logger.info('响应状态码:' + str(r.status_code))
        #     # logger.info('响应头信息：' + str(r.headers))
        #     # logger.info('响应数据：' + r.text)
        # except:
        #     pass

        # print(kwargs)
        for dd in tl:
            cv = dd['value']
            if dd['ctype'] == 'json':
                if str(r.status_code).startswith('20') and 'Content-Type' in r.headers and r.headers[
                    'Content-Type'].startswith('application/json'):
                    vak = cv.split(':')
                    ke = vak[0].split('.')
                    re = r.json()
                    for i in ke:
                        if i.isdigit():
                            if len(re) > int(i):
                                re = re[int(i)]
                            else:
                                raise Exception('校验结果时，无法提取字段：' + vak[0])
                        else:
                            if not isinstance(re, dict) or re.get(i) is None:
                                raise Exception('校验结果时，无法提取字段：' + vak[0])
                            else:
                                re = str(re[i])
                    # if str(vak[1]).lower()=='true':
                    #     if not isinstance(re,str) and len(re)>0
                    if isinstance(re, str):
                        if str(re).strip() != str(vak[1]).strip():
                            raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % (str(vak[1]), str(re)))
                        else:
                            logger.info(cv + '，数据校验成功')
                    else:
                        if str(vak[1]).lower() == 'true':
                            if len(re) > 0:
                                logger.info(cv + '，数据校验成功')
                            else:
                                raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % ('存在数据', '没有数据'))
                        elif str(vak[1]).lower() == 'false':
                            if len(re) == 0:
                                logger.info(cv + '，数据校验成功')
                            else:
                                raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % ('不存在数据', '有数据'))
                        else:
                            raise Exception('校验结果出错，期望结果：%s,实际结果：%s' % (str(vak[1]), str(re)))
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是键值对：' + cv)
            elif dd['ctype'] == 'contain':
                if str(r.status_code).startswith('20') and len(r.text) > 0:
                    if r.text.find(cv) == -1:
                        return Exception('响应结果不包含：' + cv)
                    else:
                        logger.info(cv + '存在，数据校验成功')
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是含有：' + cv)
            elif dd['ctype'] == 'match':
                if str(r.status_code).startswith('20') and len(r.text) > 0:
                    if r.text != cv:
                        return Exception('响应结果不完全匹配：' + cv)
                    else:
                        logger.info(cv + '，数据校验成功')
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是匹配：' + cv)
            elif dd['ctype'] == 'status':
                if str(r.status_code) != str(cv):
                    raise Exception('接口响应代码不正确，为' + str(r.status_code) + '，期望：' + str(cv))
                else:
                    logger.info(cv + '状态码匹配，数据校验成功')
            elif dd['ctype'] == 'bool':
                if str(r.status_code).startswith('20'):
                    is_ok = True
                    ress = '有'
                    if cv.lower() != 'true':
                        is_ok = False
                        ress = '无'
                    if is_ok == len(r.text) > 0:
                        logger.info('结果数据%s，校验成功' % ress)
                    else:
                        raise Exception('结果数据%s，校验失败，结果：%s' % (ress, r.text))
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text)
            elif dd['ctype'] == 'not':
                if str(r.status_code).startswith('20') and len(r.text) > 0:
                    if r.text.find(cv) == -1:
                        logger.info(cv + '不匹配，数据校验成功')
                    else:

                        return Exception('响应结果不包含：' + cv)
                else:
                    raise Exception('请求结果出错，接口响应代码不正确，为' + str(r.status_code) + ',响应结果为：' + r.text + '期望是含有：' + cv)
        tva = set()
        if csql is not None:
            ac = p_str2split(csql, ';')
            try:
                for i, j in ac.items():
                    i = i.split('_')[1]
                    if gg.get(i) is not None:
                        va = gg.get(i)

                        vv1 = _check_para(j)
                        va.check(vv1)
                        tva.add(va)
                        # va.commit()
                    else:
                        raise Exception(i + '无此方法，请查询')
                for i in tva:
                    i.commit()
            except Exception as e:
                for i in tva:
                    i.rollback()
                raise Exception('运行sql校验失败,' + str(e))
        return r

    if is_step:
        return check_step
    else:
        return check


@log
def _check_para(ss, gg):
    if ss is None:
        return None
    ss = str(ss)
    # 取出值${}
    pa = p_get_data_re(ss)
    # if len(pa) == 1 and ss == "${%s}" % pa[0]:
    #     if pa[0] in global2:
    #         return global2[pa[0]]

    if len(pa) > 0:
        for i in pa:
            i2 = i.strip()
            if gg.get(i2) is not None:
                ss = ss.replace('${%s}' % i, str(gg.get(i2)))
            elif '.' in i:
                ke = i.split('.')
                re = ke[0]
                if re in gg:
                    re = gg[re]

                    for j in ke:
                        if j.startswith('para_'):
                            continue
                        if j.isdigit():
                            if len(re) > int(j):
                                re = re[int(j)]
                            else:
                                raise Exception('无法提取字段：' + i)
                        else:
                            if not isinstance(re, dict) or re.get(j) is None:
                                raise Exception('无法提取字段：' + i)
                            else:
                                re = re[j]
                    ss = ss.replace('${%s}' % i, p_obj2json(re))
                else:
                    raise Exception(re + ',不在方法中')
            elif '_' in i and '随机' in i:
                ke = i.split('_')
                if len(ke) > 1 and ke[2].isdigit():
                    re = ke[0]
                    rn = ke[1]
                    try:
                        if re == '随机字母':
                            a = get_random_element(rn)
                        elif re == '随机数字':
                            a = get_random_int(rn)
                        else:
                            a = get_random_int_element(rn)

                        a = str(a)
                        if len(ke) == 3:
                            paa = ke[2]
                            gg[paa] = a
                        ss = ss.replace('${%s}' % i, a)
                    except:
                        raise Exception(rn + '无法获取,' + str(i))
                else:
                    raise Exception(i + ',格式输入操作，应该是:随机xx_n_name')
            elif '%' in i and '日期' in i:
                try:
                    i1 = i.strip()[2:]
                    i2 = i1.split('_')
                    ss1 = ''
                    if i2[1] == 'n':
                        if len(i2) == 5:
                            ss1 = p_get_fix(i2[4], i2[3], i2[2], f=i2[0])
                        else:
                            ss1 = p_get_fix(f=i2[0])
                    elif i2[1] == 'l':
                        if len(i2) == 5:
                            ss1 = p_get_month_lastday(i2[4], i2[3], i2[2], f=i2[0])
                        else:
                            ss1 = p_get_month_lastday(f=i2[0])
                    elif i2[1] == 'f':
                        if len(i2) == 5:
                            ss1 = p_get_month_fristday(i2[4], i2[3], i2[2], f=i2[0])
                        else:
                            ss1 = p_get_month_fristday(f=i2[0])
                    elif i2[1] == 's':
                        if len(i2) == 7:
                            ss1 = p_get_fix(i2[6], i2[5], i2[4], f=i2[0], t=p_form2time(i2[2], i2[3]))
                        else:
                            ss1 = p_get_fix(f=i2[0], t=p_form2time(i2[2], i2[3]))
                    elif i2[1] == 'p':
                        i3 = _check_para(i2[2])
                        if len(i2) == 7:
                            ss1 = p_get_fix(i2[6], i2[5], i2[4], f=i2[0], t=p_form2time(i3, i2[3]))
                        else:
                            ss1 = p_get_fix(f=i2[0], t=p_form2time(i3, i2[3]))
                    ss = ss.replace('${%s}' % i, ss1)

                except Exception as e:
                    raise Exception('日期转换错误，' + str(i) + ',' + str(e))

        return ss

    else:
        return ss
