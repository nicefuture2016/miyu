#-*- coding:utf-8 -*-
'''
 * @author LLc
 * @version 1.0 : 2019/6/5 11:45
 * @Project : miyu
 * @Software: PyCharm
'''
'''
"https://f.app1212.com/readImg.form?filename=1549207792482"
import re
url = "https://f.app1212.com/readImg.form?filename=1549207792482;test;https://hsdsa.app1212.com/readImg.form?filename=1555078728890;;;;;https://hsdsa.app1212.com/readImg.form?filename=1555021728890"
#groupdict = re.search("(?<=filename=)(?P<timestamp>\d+)",url).groupdict()
time_list = re.findall("https://[^/]*/readImg.form\?filename=(\d+)",url)

for time in time_list:
    newurl = 'https://img-1256517108.cos.ap-chengdu.myqcloud.com/%s.jpg'%time
    url = re.sub("https://[^/]*/readImg.form\?filename=%s"%time,newurl,url)
print(url)

'''

import time,hashlib,requests

def md5(str):
    m = hashlib.md5()
    b = str.encode(encoding='utf-8')
    m.update(b)
    md5sum = m.hexdigest()
    return md5sum

# 搜索
app_key = 'lovekit'
app_secret = '0I7UwwU1Tiq3mjiNeI72'
timestamp = int(time.time())

# 请求参数 中文参数需要urlencode，%E4%BD%A0%E5%A5%BD=你好
query_params = "page=3"

# 拼接 app_secret + query_params，然后进行MD5加密，转大写
sign = md5(app_secret + query_params).upper()
print(sign)

params = {
    'sign' : sign,
    'app_key' : 'lovekit',
    'timestamp' : timestamp,
    'page' : 3
}

# 发送请求
response = requests.get('http://127.0.0.1:8000/api/v1/lesson/30/cid/20/',params=params)
print(response.text)
