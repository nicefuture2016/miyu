from django.conf import settings
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
import logging,redis
import hashlib,time
logger = logging.getLogger('miyu.api.common.func')

def jieba_analyse(jieba_list):
    '''
    :param jieba_list: jieba分词
    :return: 分词列表
    '''
    result = []
    if len(jieba_list) == 1:
        result.append(jieba_list[0])
    else:
        for elment in jieba_list[1:]:
            if len(elment) >= 2:
                result.append(jieba_list[0]+elment)


        jieba_list.pop(0)
        jieba_analyse(jieba_list)

    return result


class SmsSender(object):
    '''
    发送登录验证短信API
    '''
    def __init__(self):
        self.appid = settings.APPID
        self.appkey = settings.APPKEY
        self.templateid = settings.TEMPLATEID
        self.sign = settings.SIGN

    def create_code(self):
        '''
        :return: 生成随机码
        '''

        code = ''
        for num in range(1, 5):
            code = code + str(random.randint(0, 9))

        return code


    def sender(self,phone):
        '''
        :param phone: 手机号
        :return: 手机验证码 or None
        '''
        ssender = SmsSingleSender(self.appid,self.appkey)

        code = self.create_code()
        params = [code, settings.SMS_TIME]
        try:
            # 发送短信
            result = ssender.send_with_param(86, phone, self.templateid, params,self.sign, extend="", ext="")

            #设置短信过期时间 2分钟
            expire = settings.SMS_TIME*60
            pool = redis.ConnectionPool(host=settings.REDIS_SERVER,port=settings.REDIS_PORT,decode_responses=True)
            conn = redis.Redis(connection_pool=pool)
            conn.set(phone,code,ex=expire)
            #conn.save()
            logger.info(result)
            if result['result'] == 0:
                return code
            else:
                logger.error(result['errmsg'])
                return None
        except Exception as e:
            logger.error(e)
            return None

    def code_checker(self,phone):
        '''
        # 检测验证码是否正确
        :param phone: 手机号
        :return: 验证码
        '''
        try:
            pool = redis.ConnectionPool(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, decode_responses=True)
            conn = redis.Redis(connection_pool=pool)

            code = conn.get(phone)
            if code:
                return code
            else:
                return None

        except Exception as e:
            logger.error(e)
            return None



def create_token(phone):
    '''
    :param phone: 用户手机号
    :return: token
    '''
    ctime = str(time.time())
    m = hashlib.md5(bytes(phone,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))

    return m.hexdigest()

def create_md5(str):
    '''
    # 生成字符串MD5值
    :param str: 字符串
    :return: md5
    '''
    m = hashlib.md5()
    b = str.encode(encoding='utf-8')
    m.update(b)
    md5sum = m.hexdigest()
    return md5sum


if __name__ == '__main__':
    #word = ['不合', '合适', '吧']
    #print(word)
    #print(jieba_analyse(word))

    #print(len(create_token('13681276946')))
    print(create_md5('LoveKitToolm39*5bysb%sye+_t$3veuqy001g9ftl#4p&1%_h8#k_f7@bole1559798722'))




