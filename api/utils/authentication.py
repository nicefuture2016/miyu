from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import time
from django.conf import settings
from api.common.func import create_md5
import logging
logger = logging.getLogger('miyu.api.utils.authentication')

class SignAuthentication(BaseAuthentication):
    """
    API签名验证
    """
    def authenticate(self, request):

        #print(request.method)

        # 获取请求参数
        sign = request._request.GET.get('sign')
        timestamp = request._request.GET.get('timestamp')
        app_key = request._request.GET.get('app_key')

        print(sign)
        # 需要携带额外参数才能继续访问：比如签名，时间戳和app_key
        if not all([sign,timestamp,app_key]) or app_key != settings.APP_KEY:
            msg = 'request error'
            raise exceptions.AuthenticationFailed(detail=msg)
        querydict = request.query_params

        print(querydict)
        querydict._mutable = True

        # 删除不用的参数以供对参数进行签名认证
        try:
            querydict.pop('sign')
            querydict.pop('timestamp')
            querydict.pop('app_key')
        except:
            pass

        query_params = querydict.urlencode()
        print(query_params,'=====')
        string = settings.APP_SECRET + query_params
        m_string = create_md5(string)
        print(m_string.upper())
        if m_string.upper() != sign:
            msg = 'signature error'
            raise exceptions.AuthenticationFailed(detail=msg)

        server_timestamp = int(time.time())
        if int(timestamp) + 30 < server_timestamp:
            msg = 'Signature Expire'
            logger.error(msg)
            raise exceptions.AuthenticationFailed(detail=msg)

    def authenticate_header(self, request):
        pass

