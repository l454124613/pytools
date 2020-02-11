# -*- coding:utf-8 -*-
# Author:lixuecheng

from requests import session, Request
from pro.core.baseClass import base_class
from pro.util.parse_msg import p_to_uri, p_addhttp,p_str2content_type
from pro.core.logger import log, logger
from pro.config.sys_config import text_type, json_type
import os
import json
from urllib3 import encode_multipart_formdata


class DoRequest(base_class):
    '''
    用于http请求
    @params need_exception 默认true，执行时，raise 异常；false，执行时，不中断，异常在方法后返回值（bool，str）
    '''
    def __init__(self,need_exception=True):
        self.s = session()
        self.s.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'

        self.e = ''
        self.req = {}
        self.req_value = None
        self.res_value = None
        self.res = {}
        self.need_exception=need_exception
        self.status=False

    @log
    def run(self, method, url,header=None, **kwargs):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param header:json,text,form,multipart,other
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.or list [filepath,filepath]. or only one file use : str filepath
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
        try:
            self.req['method'] = method
            self.req['url'] = p_addhttp(url)
            self.req['headers'] = self.s.headers

            if kwargs.get('data') is not None:
                d = kwargs.get('data')
                if isinstance(d, bytes):
                    self.req['data'] = d.encode('utf8')
                else:
                    if isinstance(d, str):
                        self.req['data'] = d
                    elif isinstance(d, dict):
                        self.req['data'] = json.dumps(d, ensure_ascii=False)
                        kwargs['data'] = self.req['data']
                    else:
                        raise Exception('请求内容是不允许的类型'+str(d))
            if kwargs.get('json') is not None:
                d = kwargs.get('json')
                if isinstance(d, bytes):
                    self.req['data'] = d.encode('utf8')
                else:
                    if isinstance(d, str):
                        self.req['data'] = d
                    elif isinstance(d, dict):
                        self.req['data'] = json.dumps(d, ensure_ascii=False)

                    else:
                        raise Exception('请求内容是不允许的类型'+str(d))
                del kwargs['json']
                kwargs['data'] = self.req['data']
            if kwargs.get('params') is not None:
                d = kwargs.get('params')
                if isinstance(d, bytes):
                    self.req['data'] = d.encode('utf8')
                else:
                    if isinstance(d, str):
                        self.req['data'] = d
                    elif isinstance(d, dict):
                        self.req['data'] = json.dumps(d, ensure_ascii=False)

                    else:
                        raise Exception('请求内容是不允许的类型'+str(d))
                del kwargs['params']
                kwargs['data'] = self.req['data']

            if kwargs.get('files') is not None and len(kwargs.get('files')) > 0:
                d = kwargs.get('files')
                dd = {}
                if isinstance(d, str):
                    if os.path.exists(d):
                        dd[os.path.basename(d)] = open(d,'rb').read()
                    else:
                        raise FileNotFoundError(d)
                if isinstance(d, list):
                    for i in d:
                        if os.path.exists(i):
                            dd[os.path.basename(i)] = open(i,'rb').read()
                        else:
                            for x in dd.values():
                                x.close()
                            raise FileNotFoundError(i)
                if isinstance(d, dict):
                    for k in d.values():
                        if isinstance(k, str):
                            raise Exception(k+'，文件应该使用open("rb").read()打开')
                    dd = d
                kwargs['files'] = dd

            if kwargs.get('headers') is not None and len(kwargs.get('headers')) > 0:
                d = kwargs.get('headers')
                if isinstance(d, dict):
                    self.req['headers'].update(d)
                elif isinstance(d, str):
                    try:
                        d = json.loads(d)
                        self.req['headers'].update(d)
                    except Exception as e:
                        raise e
                else:
                    raise Exception(
                        '请求头信息不正确，请检查，使用：{"xxx": xxx, "xxxx": xxxx}')

            self.req['proxies'] = None
            if kwargs.get('proxies') is not None and len(kwargs.get('proxies')) > 0:
                d = kwargs.get('proxies')
                if isinstance(d, dict):

                    self.req['proxies'] = d
                elif isinstance(d, str):
                    if d.startswith('http'):
                        self.req['proxies'] = {"http": d, "https": d}
                    else:
                        self.req['proxies'] = {
                            "http": 'http://'+d, "https": 'http://'+d}
                else:
                    raise Exception(
                        '代理格式不正确，请检查，使用：{"http": http://xxxx, "https": http://xxxx}')
                del kwargs['proxies']
            # print(self.req)
            if header is not None:
                header = p_str2content_type(header)
                if header:
                    kwargs['headers']['Content-Type']=header
                    self.req['headers']['Content-Type']=header
                    
                else:
                    encode_data = encode_multipart_formdata(json.loads(self.req['data']))
                    kwargs['headers']['Content-Type']=encode_data[1]
                    self.req['headers']['Content-Type']=encode_data[1]
                    self.req['data']=encode_data[0]
                    kwargs['data']=encode_data[0]
                    
                    
                    
                
            logger.info(str(self.req))
            kwargs['method'] = method
            kwargs['url'] = p_addhttp(url)
            req = Request(**kwargs)
            self.req_value = self.s.prepare_request(req)
            self.status=True
   
            return True,''

        except Exception as e:
            if self.need_exception:
                self.status=False
                raise e
            else:
                self.status=False
                return False,str(e)
                

            
            # print(self.e)
            
    @log
    def add_session_headers(self,dict_headers):
        self.s.headers.update(dict_headers)

    def commit(self):
        try:
            if self.status:

                self.res_value = self.s.send(
                    self.req_value, proxies=self.req['proxies'])
                # print(dir(self.res_value))
                self.res['status_code'] = str(self.res_value.status_code)
                self.res['content'] = self.res_value.content
                self.res['elapsed'] = str(self.res_value.elapsed)
                self.res['encoding'] = str(self.res_value.encoding)
                self.res['history'] = self.res_value.history
                self.res['reason'] = str(self.res_value.reason)
                self.res['headers'] = self.res_value.headers
                self.res['url'] = str(self.res_value.url)
                # self.res['headers']=str(self.res_value.headers)
                logger.info(self.res)
                self.status=True
                return True,''
            else:
                if self.need_exception:
                    raise Exception("run方法执行错误，当前方法无法执行")
                else:
                    self.status=False
                    return False,"run方法执行错误，当前方法无法执行"

        except Exception as e:
            if self.need_exception:
                self.status=False
                raise e
            else:
                self.status=False
                return False,str(e)

    def value(self, encoding='utf8'):
        if self.status:
            if 'Content-Type' in self.res['headers']:
                a = self.res['headers']['Content-Type'].split(';')
                if a[0].strip() in json_type:

                    if len(a) == 2 and a[1].strip().startswith('charset='):
                        type = a[1].strip().replace('charset=', '')
                        text = self.res['content'].decode(type)

                        return 'json',self.res['headers']['Content-Type'], json.loads(text)
                    else:

                        return 'json',self.res['headers']['Content-Type']+'; charset=utf-8', json.loads(self.res['content'].decode('utf-8'))
                elif a[0].strip() in text_type:
                    if len(a) == 2 and a[1].strip().startswith('charset='):

                        type = a[1].strip().replace('charset=', '')
                        text = self.res['content'].decode(type)

                        return 'text',self.res['headers']['Content-Type'], text
                    else:

                        return 'text',self.res['headers']['Content-Type']+'; charset=utf-8', self.res['content'].decode('utf-8')
                else:

                    return 'other',self.res['headers']['Content-Type'], self.res['content']

            else:

                return None,None, self.res['content']
        else:
            if self.need_exception:
                    raise Exception("请求执行错误，当前方法无法执行")
            else:
                self.status=False
                return False,"请求执行错误，当前方法无法执行"
            

    def close(self):
        self.s.close()

    def check(self, fn):
        fn(self.res)

    def _is_empty(self, ss):
        if ss is None or ss.strip() == '' or ss.strip() == b'':
            return True
        return False

    def __del__(self):
        self.close()


# d = DoRequest()
# d.run('post', 'https://paytest.ciicsh.com/auth1/authenticate/login',
#       data={"userId": "13800123021", "password": "AAAaaa111"}, headers={'Content-Type': 'application/json;charset=UTF-8'})
# d.commit()
# print(d.value()[2]['message'])
# print('-'*40)
# d = DoRequest(False)
# print(d.run('post', 'https://paytest.ciicsh.com/auth/authenticate/login',
#       data={"userId": "13800123021", "password": "AAAaaa111"}))
# print(d.commit())
# print(d.value())
