#from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from django.http.response import HttpResponse
from .models import CategoryParent,CategoryChild,ShuYu,CategoryLesson,CategoryLessonChild,Lesson
from api.utils.serializer import ParentSerializer,ChildSerializer,ShuYuSerializer,ParentLessonSerializer,LessonSerializer,JSONWebTokenSerializer,LessonContentSerializer
from rest_framework import status
from api.utils.pagination import MyPageNumberPagination
from api.utils.filters import ShuYuFilter
from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework
from rest_framework_jwt.views import JSONWebTokenAPIView
from django.conf import settings
from django.db.models import Q
from .models import User
import redis,jieba,operator
from functools import reduce
from api.utils.throttle import DefaultThrottle,DataThrottle
from rest_framework_jwt.settings import api_settings
from api.common.func import jieba_analyse
from api.utils.authentication import SignAuthentication
from api.common.func import SmsSender,create_token
import logging
logger = logging.getLogger('miyu.api.views')


class Banner(APIView):
    '''
    获取Banner图片地址
    '''
    throttle_classes = [DefaultThrottle,]

    def get(self,request, *args,**kwargs):

        url  = settings.COS + settings.BANNER

        data = {'result': 10000,'img': url }


        return JsonResponse(data)

class GetSmsCodeView(APIView):
    '''
    获取验证码API
    '''
    throttle_classes = [DataThrottle, ]

    def post(self,request, *args,**kwargs):

        data = {'result':10000,'msg':'success'}

        sender = SmsSender()
        phone = request._request.POST.get('phone')

        code = sender.sender(phone)

        if not code:
            data['result'] = 10001
            data['msg'] = 'fail'

        return JsonResponse(data)


class LoginWithJsonWebToken(JSONWebTokenAPIView):

    serializer_class = JSONWebTokenSerializer

class LoginView(APIView):
    '''
    用户使用手机&验证码 登录
    '''

    throttle_classes = [DataThrottle, ]

    def post(self, request, *args, **kwargs):
        '''
        :param request: phone code
        :param args:
        :param kwargs:
        :return:
        '''
        ret = {'code':10000,'msg':None}

        phone = request._request.POST.get('phone')
        code = request._request.POST.get('code')

        sender = SmsSender()
        #获取redis中的验证码
        code_in_redis = sender.code_checker(phone)

        # 判断验证码是否正确
        if code == code_in_redis:
            token = create_token(phone)
            user, created = User.objects.get_or_create(phone=phone)
            user.token = token

            ret['msg'] = '登录成功'
            ret['token'] = token
            ret['role'] = user.role
            ret['phone'] = phone
            user.save()
        else:
            ret['msg'] = '登录失败'
            ret['code'] = 10001
        return JsonResponse(ret)


class ParentView(APIView):

    #authentication_classes =  [SignAuthentication,]

    def get(self, request, *args,**kwargs):
        category = CategoryParent.objects.all().order_by('level')
        serializer = ParentSerializer(instance=category, many=True)
        return Response(serializer.data)

class ChildView(APIView):

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):

        cid = request._request.GET.get('cid')

        child_object = CategoryChild.objects.get(pk=cid)
        child = child_object.shuyu.all().order_by('-updated')
        category = child_object.name
        # 创建分页对象
        pg = MyPageNumberPagination()
        # 获取分页的数据
        page_child = pg.paginate_queryset(queryset=child,request=request,view=self)

        # 对数据进行序列化
        serializer = ShuYuSerializer(instance=page_child, many=True)

        # 搜索排行+1
        try:
            pool = redis.ConnectionPool(host=settings.REDIS_SERVER,port=settings.REDIS_PORT,decode_responses=True)
            conn = redis.Redis(connection_pool=pool)
            conn.zincrby(settings.SEARCH_RANK,category,1)
        except Exception as e:
            logger.error(e)

        #return Response(serializer.data)
        return pg.get_paginated_response(serializer.data)

class SearchRank(APIView):

    def get(self, request, *args,**kwargs):
        data = {
            'result':[],
            'desc':'top 20 search category',
            'info':'success',
            'code':10000
        }
        try:
            pool = redis.ConnectionPool(host=settings.REDIS_SERVER,port=settings.REDIS_PORT,decode_responses=True)
            conn = redis.Redis(connection_pool=pool)
            rank = conn.zrevrange(settings.SEARCH_RANK,0,19,withscores=True)
            for category in rank:
                childid = CategoryChild.objects.filter(name=category[0]).first().id
                data['result'].append(
                    {
                        'id':childid,
                        'name':category[0],
                        'search':category[1]
                    }
                )
        except Exception as e:
            logger.error(e)
            data['code'] = 10001
            data['info'] = 'internal error'

        return Response(data)

class ShuYuSearchView(APIView):

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):

        params = request.query_params
        if not params:

            return JsonResponse(
                {
                    'code':10001,
                    'msg':'Method Not Allowed'
                }
            )
        query_match = []
        girlsay = params.get('girlsay')

        ret = jieba.lcut(girlsay, cut_all=True)

        result = jieba_analyse(ret)

        for elment in result:
            query_match.append(Q(girlsay__icontains=elment))

        #print(query_match,girlsay,result)
        #获取所有数据
        shuyu = ShuYu.objects.filter(reduce(operator.or_, query_match))
        #print(shuyu)
        #创建分页对象
        pg = MyPageNumberPagination()
        #获取分页的数据
        page_shuyu = pg.paginate_queryset(queryset=shuyu,request=request,view=self)
        #对数据进行序列化
        serializer = ShuYuSerializer(instance=page_shuyu,many=True)

        return pg.get_paginated_response(serializer.data)
        #return Response(ser.data)


class ShuYuViewSet(viewsets.ModelViewSet):

    queryset = ShuYu.objects.all().order_by('id')
    serializer_class = ShuYuSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = ShuYuFilter
    search_fields = ('girlsay')



class ParentLessonView(APIView):

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):
        category = CategoryLesson.objects.all().order_by('level')
        serializer = ParentLessonSerializer(instance=category, many=True)
        return Response(serializer.data)

class LTJXView(APIView):

    '''
    网上撩妹&聊天教学
    '''

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):

        child_name = '网上撩妹'

        child_object = CategoryLessonChild.objects.get(name=child_name).lesson.all().order_by('-created')


        pg = MyPageNumberPagination()
        # 获取分页的数据
        page_child_lesson = pg.paginate_queryset(queryset=child_object,request=request,view=self)

        # 对数据进行序列化
        serializer = LessonSerializer(instance=page_child_lesson, many=True)

        return pg.get_paginated_response(serializer.data)

class MRJXView(APIView):

    '''
    每日优选
    '''

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):

        child_name = '精选文章'

        child_object = CategoryLessonChild.objects.get(name=child_name).lesson.all().order_by('-created')


        pg = MyPageNumberPagination()
        # 获取分页的数据
        page_child_lesson = pg.paginate_queryset(queryset=child_object,request=request,view=self)

        # 对数据进行序列化
        serializer = LessonSerializer(instance=page_child_lesson, many=True)

        return pg.get_paginated_response(serializer.data)

class KCTJView(APIView):

    '''
    课程推荐
    '''

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):

        child_name = '极限话术高级版'

        child_object = CategoryLessonChild.objects.get(name=child_name).lesson.all().order_by('-created')


        pg = MyPageNumberPagination()
        # 获取分页的数据
        page_child_lesson = pg.paginate_queryset(queryset=child_object,request=request,view=self)

        # 对数据进行序列化
        serializer = LessonSerializer(instance=page_child_lesson, many=True)

        return pg.get_paginated_response(serializer.data)


class ZYFLKCView(APIView):

    '''
    主页分类课程
    '''

    def get(self, request, *args, **kwargs):
        category = CategoryLesson.objects.filter(role=1).order_by('level')
        serializer = ParentLessonSerializer(instance=category, many=True)
        return Response(serializer.data)

class ChildLessonView(APIView):

    #authentication_classes = [SignAuthentication, ]

    def get(self, request, *args,**kwargs):

        # 总分类id
        pk = kwargs.get('pk')
        # 子分类id
        cid = kwargs.get('cid')

        # 获取大分类对象
        pk_object = CategoryLesson.objects.get(pk=pk)

        print(pk_object.name,pk,cid)
        # 获取子分类对象
        category_obj = pk_object.Lessonchild.get(pk=cid).lesson.all()

        #lesson = category_obj.lesson.get(pk=lid).all()
        # 创建分页对象
        pg = MyPageNumberPagination()
        # 获取分页的数据
        page_child = pg.paginate_queryset(queryset=category_obj,request=request,view=self)

        # 对数据进行序列化
        serializer = LessonSerializer(instance=page_child, many=True)

        return pg.get_paginated_response(serializer.data)

class LessonContentView(APIView):

    #authentication_classes = [SignAuthentication, ]

    '''
    返回课程内容
    '''
    def get(self, request, *args,**kwargs):

        # 课程ID
        pk = kwargs.get('pk')

        # 获取大分类对象
        lesson_object = Lesson.objects.get(pk=pk)

        # 对数据进行序列化
        serializer = LessonContentSerializer(instance=lesson_object,)

        return Response(serializer.data)

class LessonLikeView(APIView):
    '''
    喜欢课程
    '''
    def get(self, request, *args,**kwargs):

        ret = {'code': 10000, 'msg': 'success'}

        # 课程ID
        pk = kwargs.get('pk')

        # 获取大分类对象
        lesson_object = Lesson.objects.get(pk=pk)

        try:
            like = lesson_object.like
            lesson_object.like = like+1
            lesson_object.save()
        except Exception as e:
            logger.error(e)
            ret['code'] = 10001
            ret['msg'] = 'fail'

        return JsonResponse(ret)

class LessonFavoriteView(APIView):
    '''
    收藏课程
    '''
    def post(self, request, *args,**kwargs):

        ret = {'code': 10000, 'msg': 'success'}

        # 课程ID
        token = request._request.POST.get('token')
        id = request._request.POST.get('id')
        print(token,id)
        # 获取当前课程对象
        lesson_object = Lesson.objects.filter(pk=id)

        try:
            user_obj = User.objects.get(token=token)
            # 添加我的收藏
            user_obj.lesson.add(*lesson_object)
            user_obj.save()
        except Exception as e:
            logger.error(e)
            ret['code'] = 10001
            ret['msg'] = 'fail'

        return JsonResponse(ret)


class LessonMyFavoriteView(APIView):
    '''
    返回我的收藏
    '''
    def post(self, request, *args,**kwargs):

        ret = {'code': 10000, 'msg': 'success'}

        # 课程ID
        token = request._request.POST.get('token')

        # 获取大分类对象
        user_object = User.objects.get(token=token)

        lesson_object = user_object.lesson.all()
        # 对数据进行序列化
        serializer = LessonSerializer(instance=lesson_object,many=True)

        return Response(serializer.data)


def data(request):

    '''
    import re
    for lesson in Lesson.objects.all():

        url = lesson.content

        time_list = re.findall("https://[^/]*/readImg.form\?filename=(\d+)", url)

        for time in time_list:
            newurl = 'https://img-1256517108.cos.ap-chengdu.myqcloud.com/%s.jpg' % time
            url = re.sub("https://[^/]*/readImg.form\?filename=%s" % time, newurl, url)
        lesson.content = url
        lesson.save()
    '''
    '''
    import re
    from urllib.request import urlretrieve
    for lesson in Lesson.objects.all():
        content  = lesson.content
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        url = re.findall(pattern, content)
        #url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content)
        if url:
            for i in url:
                if  'filename' in i:
                    time = i.split('=')[1]
                    urlretrieve(i, '/content/' + time + '.jpg')
        time = imgurl.split('=')[1]
        if time:
            from urllib.request import urlretrieve
            urlretrieve(imgurl, '/content/' + time + '.jpg')
        else:
            print(imgurl)

    '''
    '''
    for i in CategoryLesson.objects.all():
        print(i.name,'==============')
        for j in i.Lessonchild.all():
            print(j.name,'***********',len(j.lesson.all()))
    '''
    '''
    from qcloud_cos import CosConfig
    from qcloud_cos import CosS3Client
    import sys
    import logging

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    secret_id = 'AKIDSnkW7haB9QXS8lk5QdmoiWIqENzFJC35'  # 替换为用户的 secretId
    secret_key = 'zmOjpiR1meIm9MMm14xdlwxo7EAtPlz6'  # 替换为用户的 secretKey
    region = 'ap-chengdu'  # 替换为用户的 Region
    token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    # 2. 获取客户端对象
    client = CosS3Client(config)

    #### 文件流简单上传
    import os
    for i in os.listdir('/content'):
        file_name = os.path.join('/content',i)
        # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
        with open(file_name, 'rb') as fp:
            response = client.put_object(
                Bucket='img-1256517108',
                Body=fp,
                Key=i,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        print(response['ETag'])
    '''
    '''
    #url = 'https://hs.app1212.com/readImg.form?filename=1555407330542'
    #from urllib.request import urlretrieve
    #urlretrieve(url, './img.jpg')

    '''
    '''
    import  itertools
    shuyu1 = ShuYu.objects.all()[0:4]
    shuyu2 = ShuYu.objects.all()[3:5]
    print(shuyu1)
    print(shuyu2)
    #shuyu = shuyu1 | shuyu2
    qiter = itertools.chain(shuyu1, shuyu2)

    for i in qiter.distinct():
        print(i)

    #print(qiter.distinct())
    '''
    '''
    shuyu_obj = ShuYu.objects.all()
    list = []
    for shuyu in shuyu_obj:
        if shuyu.content.startswith('<p>女'):
            id = shuyu.id
            abc = shuyu.content.split('</p>')[0].strip()
            #up = ShuYu.objects.get(pk=id)
            #up.girlsay = abc
            #up.save()
            shuyu.girlsay = abc
            shuyu.save()
            #shuyu.update(girlsay=abc)
            #print(shuyu.content.split('</p>')[0])
            list.append(abc)
            #print(abc)
            #shuyu.updated(girlsay=shuyu.content)
    print(len(list))
    '''
    import pymysql
    #categorylessonchild_obj = CategoryLessonChild.objects.all()
    ## 打开数据库连接，不需要指定数据库，因为需要创建数据库
    #conn = pymysql.connect('182.254.146.59', user="root", passwd="AKL2wkzV4DHAJdrp")
    #conn.select_db('lass')
    #cur = conn.cursor()
    #cur.execute("select * from tbl_essay_type")
    #res = cur.fetchall()
    #for row in res:
    #    print(row[1])
    #    for i in categorylessonchild_obj:
    #        if row[1] == i.name:
    #            CategoryLessonChild.objects.filter(name=i.name).update(cid=row[0])
#
    #    #Lesson.objects.create(**{'title': row[3],'content': row[4],'lessontype':row[2],'lessonimg':row[5]})
    #conn.close()

    #lesson_obj = Lesson.objects.all()
    #for lesson in lesson_obj:
        #if '：' in lesson.title:
            #categoty = lesson.title.split('：')[0].strip()
            #print(lesson.title)
            #CategoryLessonChild.objects.create(**{'name': categoty})
            #lessonchild_object, created = CategoryLessonChild.objects.get_or_create(name=categoty)

    #categorylesson_obj = CategoryLesson.objects.all()

    #for i in categorylesson_obj:
        #lessonchild_object, created = CategoryLessonChild.objects.get_or_create(name=i.name)
    #categorylesson_obj = CategoryLesson.objects.all()
    #categorylessonchild_obj = CategoryLessonChild.objects.all()

    #for i in categorylessonchild_obj:
        #print(i.name,'=====')

        #if not len(i.lesson.all()):
            #print(i.name)
        #for j in i.lesson.all():
            #print(j.title)
    #print(data)

    #for category in categorylessonchild_obj:

        #cid = category.cid
        #if not cid:

            #print(category.name)

            #lesson_obj = Lesson.objects.filter(title__startswith=category.name)

            #category.lesson.add(*lesson_obj)
            #cid_obj = Lesson.objects.filter(lessontype=cid)

            #category.lesson.add(*cid_obj)

        #print(category.name,'================')

        #for i in category.Lessonchild.all():
            #print(i.name)
        #print(category.name)
        #if data.get(category.name):

            #for i in data[category.name]:
                #print(i)
                #categorylessonchild_obj = CategoryLessonChild.objects.filter(name=i)
                #category.Lessonchild.add(*categorylessonchild_obj)
        #categorylessonchild_obj = CategoryLessonChild.objects.filter(name=category.name)
        #for child in categorylessonchild_obj:


            #if category.name == child.name:

                #print(category.name,child.name)


        #cid = child.myid

        #chat_obj = ShuYu.objects.filter(cid=cid)

        #category.Lessonchild.add(*categorylessonchild_obj)

        #child.save()
    '''
    child_obj = CategoryChild.objects.all()

    for child in child_obj:

        cid = child.myid

        chat_obj = ShuYu.objects.filter(cid=cid)

        child.shuyu.add(*chat_obj)

        child.save()
    '''
    '''
    parent_object = CategoryParent.objects.all()

    for parent in parent_object:

        print(parent.name,'======================')


        for child in parent.child.all():

            if len(child.shuyu.all()):
                print(child.name,':',len(child.shuyu.all()))
    '''

    '''
    import jieba

    word = "你怎么还不睡"

    #mytext = jieba.cut(word)

    mytext = " ".join(jieba.cut(word))
    print(mytext)
    print('你' in '<p>女：你太有才了&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    '''
    return HttpResponse(111)