#-*- coding:utf-8 -*-
'''
 * @author LLc
 * @version 1.0 : 2019/5/28 10:52
 * @Project : miyu
 * @Software: PyCharm
'''
'''
def jwt_response_payload_handler(token, user=None, request=None):
    """
    登录成功后自定义返回
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        "code":2000,
        'user': user,
        "data": {
            "token": token
        }
    }
'''