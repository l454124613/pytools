# -*- coding:utf-8 -*-
# Author:lixuecheng
from selenium import webdriver
import time
import os
from pro.core.logger import log, logger
from pro.util.parse_msg import p_addhttp
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from pro.config.sys_config import tag_type


class DoSelenium:
    '''
    方法用于使用selenium

    @params driver_path chrome_driver的地址

    @params is_headless 默认false ；true 不显示操作页面；false 显示页面
    '''
    @log
    def __init__(self, driver_path, is_headless=False):
        self.start_time = time.time()
        self.run_start_time = 0
        self.status = {'state': True, 'e': []}
        self._is_inframe = False
        self._windows_handles_set = list()
        self.local_name_dict={}

        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(
                '--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
            # chrome_options.add_argument(
            #     '--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
            chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
            # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            if is_headless:
                chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面
            logger.info(
                '\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            logger.info('chrome正在启动中...')
            self._driver = webdriver.Chrome(
                executable_path=driver_path, options=chrome_options)
            self.run_start_time = time.time()
            logger.info('chrome启动完成，用时：' +
                        str(self.run_start_time-self.start_time))
        except Exception as e:
            self.status['e'].append({'ex': e, 'epath': 'init'})
            self.status['state'] = False
            self._driver = None
            logger.error('chrome启动失败：'+str(e))
            raise e

    def get_driver(self):
        '''
        @return driver的对象
        '''
        return self._driver

    def get_status(self):
        '''
        @return 当前的运行状态
        '''
        return self.status

    def options(self):
        '''
        @return 配置的对象
        '''
        if self.status['state']:
            return opt(self._driver)

    def into_frame(self, path, des, local=None, n=1):
        '''
        @params path 定位的路径

        @params des 定位的描述

        @params local 定位的方法

        @params n 定位多个定位的其中的序号

        @return 方法

        '''
        ele = self.element(path, des, local, n)
        self._driver.switch_to_frame(ele)
        return self

    def operate(self):
        '''
        @return 控制流程的操作
        '''
        return ope(self._driver, self.status)

    @log
    def action(self, path, des=None, local=None, n=1, sleep_time=0.9, path2=None, des2=None, local2=None, n2=1):
        '''
        @params path 元素的定位路径

        @params des 元素的描述

        @params local 元素的定位方式

        @params n 多个定位的序号

        @params sleep_time 默认0.9s 操作前 睡眠的时间

        @params path2 元素2的定位路径

        @params des2 元素2的描述

        @params local2 元素2的定位方式

        @params n2 元素2多个定位的序号

        @return 元素的操作


        '''
        if self.status['state']:
            time.sleep(sleep_time)
        if path is None :
            return act(self._driver, None, self.status, None, self._is_inframe)
        else:
            ele = self.element(path, des, local, n)
            ele2 = None
            if path2 is not None:
                ele2 = self.element(path2, des2, local2, n2)
            return act(self._driver, ele, self.status, ele2, self._is_inframe)

    @log
    def element(self, path, des, local=None, n=1, xr=0, need_screen=None):
        '''
        @params path 元素的定位路径

        @params des 元素的描述

        @params local 元素的定位方式

        @params n 多个定位的序号

        return
            bool false 没有定位到唯一元素
            obj  str为报错，list是很多元素或者n输入操作
            des  描述

        '''

        # 检查新增windows——handle
        # print('now',des)
        wd = self._driver.window_handles

        # print(wd)
        for i in wd:
            # 新增窗口
            if i not in self._windows_handles_set:
                self._driver.switch_to.window(i)
                self._windows_handles_set.append(i)
                logger.info("切换窗口："+self._driver.title)
                time.sleep(1)
                break
        else:
            # 关闭窗口
            if self._driver.current_window_handle not in wd:
                self._windows_handles_set.remove(
                    self._driver.current_window_handle)
                self._driver.switch_to.window(
                    self._windows_handles_set[len(self._windows_handles_set)-1])
            else:
                self._driver.switch_to.window(
                    self._driver.current_window_handle)

        if des is None:
            if path.strip() in self.local_name_dict:
                des=self.local_name_dict[path.strip()]
            else:
                des=str(path)
        else:
            des = str(des)
            self.local_name_dict[path.strip()]=des
            
        
        path = str(path)
        if local is None:
            if path.strip().lower().startswith('//') or  path.strip().lower().startswith('/html') or '@' in path:
                local=By.XPATH
            elif '.' in path or '#' in path or ']' in path or '>' in path:
                local=By.CSS_SELECTOR
            elif path+'</a>' in self._driver.page_source:
                local=By.LINK_TEXT
            elif  path in tag_type:
                local=By.TAG_NAME
            elif   'id="{}"'.format(path.strip()) in self._driver.page_source:
                local=By.ID
            elif 'name="{}"'.format(path.strip()) in self._driver.page_source:
                local=By.NAME
            else:
                local=By.CLASS_NAME
            
        try:
            ca = self._driver.find_elements(by=local, value=path)
            # print(ca)
            if len(ca) > 0:
                if n > 0:
                    if len(ca) <= n:
                        sty = ca[n-1].get_attribute('style')
                        self._driver.execute_script(
                            'arguments[0].setAttribute("style","background-color:grey")', ca[n-1])
                        if need_screen is not None:
                            try:
                                self._driver.save_screenshot(need_screen)
                            except Exception as e:
                                logger.warning(
                                    '截图失败，地址：'+need_screen+',原因：'+str(e))
                        self._driver.execute_script(
                            'arguments[0].setAttribute("style","'+str(sty)+'background-color:grey''")', ca[n-1])

                        return True, ca[n-1], des
                    else:
                        raise Exception(
                            str(des)+':'+str(local)+'->'+str(path)+'('+str(n)+'),选择的值超出查找上限，共'+str(len(ca)))
                else:
                    return False, ca, des
            else:
                raise NoSuchElementException(
                    str(des)+':'+str(local)+'->'+str(path)+'('+str(n)+')')
        except NoSuchElementException as e:
            if xr>10:
                self.status['e'].append({'ex': e, 'epath': 'element'})
                self.status['state'] = False
                return False, str(e), des
            else:
                xr+=1
                time.sleep(0.9)
                return self.element(path,des,local,n,xr)
        except Exception as e:
            self.status['e'].append({'ex': e, 'epath': 'element'})
            self.status['state'] = False
            return False, str(e), des
            

    def get_value(self, path,des, local=None, n=1, sleep_time=0.5):
        '''
        @params path 元素的定位路径

        @params des 元素的描述
        
        @params local 元素的定位方式
        
        @params n 多个定位的序号
        
        @params sleep_time 默认0.5s 操作前 睡眠的时间
        
        @return 或者值的对象
        
        '''
        if self.status['state']:
            time.sleep(sleep_time)
        if path is None and des is None:
            ele = None
        else:
            ele = self.element(path, des, local, n)
        return che(self._driver, ele, self.status,self._is_inframe)

    def __del__(self):
        if len(self.status['e']) > 0:
            print(self.status['e'])


class opt:
    '''
    用于配置
    @params driver 驱动对象
    '''
    def __init__(self, driver):
        self._driver = driver

    def wait_time(self, n=1):
        '''
        隐身等待方式 
        @params  n 等待的时间
        '''
        self._driver.implicitly_wait(n)

    def load_page_timeout(self, n=30):
        '''
        页面加载超时时间
        @params  n 等待的时间
        '''
        self._driver.set_page_load_timeout(n)

    def maximize_window(self):
        '''
        屏幕最大化

        '''
        self._driver.maximize_window()

    def minimize_window(self):
        '''
        屏幕最小化

        '''
        self._driver.minimize_window()


class che:
    '''
    
    用于获得元素的值
    
    @params driver 驱动对象
    
    @params element 元素对象
    
    @params status 当前运行状态
    
    @params is_inframe 是否进入frame
    
    '''
    def __init__(self, driver, element, status,is_inframe):

        self.status = status
        self._is_inframe=is_inframe
        self._driver = driver
        if element is not None:
            self.element = element[1]
            if not element[0]:
                self.status['state'] = False
                if isinstance(element[1], list):
                    self.status['e'].append(
                        {'ex': Exception('所得的元素有多个值'), 'epath': 'action_init'})
            else:
                self.is_select = element[1].is_selected()
            
                self.is_enabled = element[1].is_enabled()
                self.is_display = element[1].is_displayed()
                self.tag_name = element[1].tag_name
            self.des = element[2]
      
        

    def text(self):
        '''
        获得元素的text的值
        '''
        v=None
        if self.status['state']:
            if self.tag_name == 'input':
                v= self.element.get_attribute('value')
            else:
                v= self.element.text
            logger.info(self.des+',获取值：'+str(v))
        if self._is_inframe:
            self._driver.switch_to.default_content()
        return v

    def attr(self, att):
        '''
        获得元素的指定属性的值
        
        @params att 属性名称
        '''
        v=None
        if self.status['state']:
            v= self.element.get_attribute(att)
            logger.info(self.des+',获取属性：'+str(att)+'：'+str(v))
        if self._is_inframe:
            self._driver.switch_to.default_content()
        return v

    def size(self):
        '''
        获得元素的尺寸
        '''
        v=None
        if self.status['state']:
            v= self.element.size
            logger.info(self.des+',获取大小：'+str(v))
        if self._is_inframe:
            self._driver.switch_to.default_content()
        return v

    def title(self):
        '''
        获得页面的标题
        
        '''
        if self._is_inframe:
            self._driver.switch_to.default_content()
        if self.status['state']:
            logger.info(self.des+',获取标题：'+str(self._driver.title))
            return self._driver.title
        else:
            return None
    def page_source(self):
        '''
        获得页面的标题
        
        '''
        if self._is_inframe:
            self._driver.switch_to.default_content()
        if self.status['state']:
            logger.info(self.des+',获取网页内容：'+str(self._driver.page_source))
            return self._driver.page_source
        else:
            return None
    def alert_text(self):
        '''
        获得提示框的值
        '''
        
        if self.status['state']:
           v=  self._driver.switch_to.alert.text
           logger.info("获得提示框的值："+v)
           return v
        else:
            return None


class act:
    def __init__(self, driver, element, status,  element2,is_inframe):
        '''
    
        用于元素操作
        @params driver 驱动对象
        @params element 元素对象
        @params status 当前运行状态
        @params element2 第二个元素对象
        @params is_inframe 是否进入frame
        '''
        # time.sleep(sleep_time)
        self._is_inframe=is_inframe
        self.status = status
        self._driver = driver
        if element is not None:
            self.element = element[1]
            if not element[0]:
                self.status['state'] = False
                if isinstance(element[1], list):
                    self.status['e'].append(
                        {'ex': Exception('所得的元素有多个值'), 'epath': 'action_init'})
            else:
                self.is_select = element[1].is_selected()
                self.is_enabled = element[1].is_enabled()
                self.is_display = element[1].is_displayed()
                self.tag_name = element[1].tag_name
            

            self.des = element[2]
        

        if element2 is not None:
            self.element2 = element2[1]
            if not element2[0]:
                self.status['state'] = False
                if isinstance(element2[1], list):
                    self.status['e'].append(
                        {'ex': Exception('所得的元素有多个值'), 'epath': 'action_init'})
            else:
                self.is_select2 = element2[1].is_selected()
                self.is_enabled2 = element2[1].is_enabled()
                self.is_display2 = element2[1].is_displayed()
                self.tag_name2 = element2[1].tag_name

            self.des2 = element2[2]
            

        # print(ele[1].get_attribute('class'))
        # print(ele[1].is_displayed())
        # print(ele[1].is_enabled())
        # print(ele[1].is_selected())
        # print(ele[1].tag_name)
        # print(ele[1].text)

    def click(self):
        '''
        元素点击
        '''
        # print(self.status)
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    self._driver.execute_script(
                        "arguments[0].click();", self.element)
                    logger.info('点击:'+self.des)
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法点击'), 'epath': 'action_click'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法点击'), 'epath': 'action_click'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def script(self, js):
        '''
        执行js脚本
        @params js js脚本
        '''
        if self.status['state']:
            self._driver.execute_script(js)
            logger.info('执行脚本：'+str(js))
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def select_value(self, val):
        '''
        元素下拉框选择值
        @params val 选择框的值<select value='?'> 问号的地方
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    if self.tag_name == 'select':
                        Select(self.element).select_by_value(val)
                    logger.info(self.des+':选择值：'+str(val))
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法选择'), 'epath': 'action_select_val'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法选择'), 'epath': 'action_select_val'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def select_text(self, val):
        '''
        元素下拉框选择值
        @params val 选择框的值<select value='1'>?</select> 问号的地方
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    if self.tag_name == 'select':
                        Select(self.element).select_by_visible_text(val)
                    logger.info(self.des+':选择：'+str(val))
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法选择'), 'epath': 'action_select_text'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法选择'), 'epath': 'action_select_text'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def deselect_value(self, val):
        '''
        取消选择元素下拉框选择值
        @params val 选择框的值<select value='?'> 问号的地方
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    if self.tag_name == 'select':
                        Select(self.element).deselect_by_value(val)
                        logger.info(self.des+':清除选择值：'+str(val))
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法选择'), 'epath': 'action_deselect_val'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法选择'), 'epath': 'action_deselect_val'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def deselect_text(self, val):
        '''
        取消元素下拉框选择值
        @params val 选择框的值<select value='1'>?</select> 问号的地方
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    if self.tag_name == 'select':
                        Select(self.element).deselect_by_visible_text(val)
                        logger.info(self.des+':清除选择：'+str(val))
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法选择'), 'epath': 'action_deselect_text'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法选择'), 'epath': 'action_deselect_text'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def deselect_all(self):
        '''
        取消全部元素下拉框选择值
      
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    if self.tag_name == 'select':
                        Select(self.element).deselect_all()
                        logger.info(self.des+':清除所有选择')
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法选择'), 'epath': 'action_deselect_all'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法选择'), 'epath': 'action_deselect_all'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def clear(self):
        '''
        清除输入框内容
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    self.element.clear()
                    logger.info(self.des+'清除内容')
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法清空'), 'epath': 'action_click'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法清空'), 'epath': 'action_click'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def send_keys(self, val):
        '''
        输入框内输入值
        @params  val 输入的值
        '''
        if self.status['state']:
            if self.is_enabled:
                self.element.send_keys(val)
                logger.info(self.des+':输入：'+str(val))
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不用，无法输入'), 'epath': 'action_click'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def double_click(self):
        '''
        元素双击
        '''
        if self.status['state']:
            if self.is_display:
                if self.is_enabled:
                    ActionChains(self._driver).double_click(
                        self.element).perform()
                    logger.info('双击:'+self.des)
                else:
                    self.status['state'] = False
                    self.status['e'].append(
                        {'ex': Exception('元素不用，无法点击'), 'epath': 'action_click'})
            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法点击'), 'epath': 'action_click'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def above(self):
        '''
        鼠标悬停在元素上
        '''
        if self.status['state']:
            if self.is_display:
                

                ActionChains(self._driver).move_to_element(
                    self.element).perform()
                logger.info(':鼠标移动到：'+self.des)

            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法移动至此'), 'epath': 'action_above'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def get_action(self):
        '''
        获得其他操作
        '''
        if self.status['state']:
            return ActionChains(self._driver)
        else:
            return None

    def move_to(self):
        '''
        把元素1拖到元素2
        '''
        if self.status['state']:
            if self.is_display and self.is_display2:

                ActionChains(self._driver).drag_and_drop(
                    self.element, self.element2).perform()
                logger.info('拖着：'+self.des+'到：'+self.des2)

            else:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': Exception('元素不可见，无法移动至此'), 'epath': 'action_move_to'})
        if self._is_inframe:
            self._driver.switch_to.default_content()

    def alert_accept(self):
        '''
        弹出框确认
        '''
        if self.status['state']:
            try:
                self._driver.switch_to.alert.accept()
                logger.info('弹出框点击确认')
            except Exception as e:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': e, 'epath': 'action_alert_accept'})

    def alert_dismiss(self):
        '''
        弹出框取消
        '''
        if self.status['state']:
            try:
                self._driver.switch_to.alert.dismiss()
                logger.info('弹出框点击取消')
            except Exception as e:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': e, 'epath': 'action_alert_dismiss'})

    def alert_send_keys(self, val):
        '''
        弹出框输入值
        @params  val  弹出框 输入值
        '''
        if self.status['state']:
            try:
                self._driver.switch_to.alert.send_keys(val)
                logger.info('弹出框输入值：'+str(val))
            except Exception as e:
                self.status['state'] = False
                self.status['e'].append(
                    {'ex': e, 'epath': 'action_alert_send_keys'})


class ope:
    '''
    方法用于控制浏览器
    @params driver 驱动对象
    @params status 当前的运行状态
    '''
    def __init__(self, driver, status):
        self._driver = driver
        self.status = status

    def back(self):
        '''
        返回到上一个页面
        '''
        if self.status['state']:
            self._driver.back()
            logger.info('浏览器返回上一页面')

    def forward(self):
        '''
        返回到前一个页面
        '''
        if self.status['state']:
            self._driver.forward
            logger.info('浏览器回到后一页面')

    def get(self, url):
        '''
        前往指定页面
        @params url 前往的链接，http的方式
        '''
        if self.status['state']:
            try:
                self._driver.get(p_addhttp(url))
                logger.info('浏览器打开网址：'+p_addhttp(url))
            except Exception as e:
                self.status['e'].append({'ex': e, 'epath': 'ope_get'})
                self.status['state'] = False

    def get_https(self, url):
        '''
        前往指定页面
        @params url 前往的链接，https的方式
        '''
        if self.status['state']:
            try:
                self._driver.get(p_addhttp(url, True))
                logger.info('浏览器打开网址：'+p_addhttp(url,True))
            except Exception as e:
                self.status['e'].append({'ex': e, 'epath': 'ope_gets'})
                self.status['state'] = False

    def refrash(self):
        '''
        刷新页面
        '''
        if self.status['state']:
            self._driver.refresh()
            logger.info('浏览器刷新')

    def wait(self, n=1):
        '''
        等待
        @params n 等待时间
        '''
        if self.status['state']:
            time.sleep(float(n))
            logger.info('浏览器等待（s）:'+str(n))

    def close(self):
        '''
        关闭当前标签页
        '''
        if len(self._driver.window_handles) == 1:
            self.quit()
        else:
            self._driver.close()
            logger.info('浏览器关闭一个窗口')

    def quit(self):
        '''
        关闭当前浏览器
        '''
        self._driver.quit()
        self.status['state'] = False
        logger.info("浏览器关闭\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        # os.system('taskkill /im chromedriver.exe /F')
        

    def get_cookies(self):
        '''
        获得当前cookies
        '''
        
        v= self._driver.get_cookies()
        logger.info('获取浏览器cookie:'+str(v))
        return v

    def set_cookie(self, val):
        '''
        添加cookie
        @params val 添加的值 格式：dict
        '''
        if isinstance(val, dict):
            self._driver.add_cookie(val)
            logger.info('添加浏览器cookie:'+str(val))
        else:
            logger.warning('cookie添加失败，参数格式错误')

    def get_screenshot(self, file_path=None):
        '''
        截屏
        @params file_path 截屏文件的路径，不填写默认无base64
        '''
        if file_path is not None:
            try:
                self._driver.get_screenshot_as_file(file_path)
            except Exception as e:
                logger.warning('截图失败,原因：'+str(e))
            return None

        else:
            return self._driver.get_screenshot_as_base64()


d = DoSelenium(r"C:\Users\lixuecheng\Envs\testall\79\chromedriver.exe")
d.operate().get('www.baidu.com')
# test1
# d.action('登录','登录',local=By.LINK_TEXT).click()
# d.action('立即注册','立即注册',local=By.LINK_TEXT).click()
# d.action('TANGRAM__PSP_4__userName','用户名',By.ID).send_keys('111111')
# print(d.get_value('TANGRAM__PSP_4__userName','用户名',By.ID).text())
# test2
d.action('登录','登录').click()
d.action('立即注册','立即注册').click()
d.action('TANGRAM__PSP_4__userName','用户名').send_keys('111111')
print(d.get_value('TANGRAM__PSP_4__userName','用户名').text())

# d.operate().get_screenshot('d:\\aa.jpg')
# d.action('kw', '', 'id').send_keys(1)
# d.action('su','','id').click()
# # d.action('kw','','id').clear()
# print(dir(ActionChains(d._driver)))


d.operate().quit()
