# -*- coding:utf-8 -*-

# report config
need_report = True
report_path = 'd:/'

# excel config
# set worksheet/工作簿设置

config_table = '配置'  # 配置sheet名称
ignore_table = ['说明']

# item=column_order(start with 1)/工作表设置，序号由1开始
name = 2  # 用例名称，必填
method = 4  # 请求方法，必填
host = 5  # 请求域名，包含端口号，必填
path = 6  # 请求路径，包含?以及后面的参数，必填
header_content_type = 8  # 请求头的content_type，选填
fixed_body = 7  # 请求的不变框架，选填
parameter = 9  # 填写参数，选填
pre_cases = 10  # 前置用例名称，用；分割，如果填写，先校验前置用例是否已运行（当前只是计划），选填
pre_operation = 11  # 前置操作，在执行用例前先执行的操作，用；分割，开头使用//不运行，选填
post_operation = 12  # 后置操作，执行完用例后，结果校验完成的操作，用；分割，开头使用//不运行，选填
response_check = 13  # 响应结果校验，用；分割，true响应代码20x，有结果；false响应代码20x，没有结果；~开头，响应体含有；！开头，响应体不包含；纯数据，匹配响应代码；含有：的键值对，提取json值；其他是完全匹配，必填
sql_check = 14  # 数据库校验，用；分割，只支持sql语句，select查询，选填
is_run = 17  # 是否可运行，是，可以，否，不可以，必填

# function config
add_header = '加入请求头'
kong = '空'
wait_second = '等待'
get_res = '提取结果值'

# 请求头配置
json_type=['application/json']
text_type=['text/html','text/plain','text/xml','application/xml']