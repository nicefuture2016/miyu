from rest_framework import serializers
from api.models import CategoryParent,CategoryChild,ShuYu,CategoryLesson,CategoryLessonChild,Lesson,User
from rest_framework_jwt.settings import api_settings
from api.common.func import SmsSender
import datetime,json
class ParentSerializer(serializers.ModelSerializer):

    child  = serializers.SerializerMethodField()

    class Meta:
        model = CategoryParent
        fields = ('id','name','info','child')

    def get_child(self,row):
        child_obj_list = row.child.all()
        ret = []

        for item in child_obj_list:
            ret.append({'name':item.name,'id':item.id})

        return ret

class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryChild
        #fields = ['shuyu']
        fields = '__all__'
        depth = 2

class ShuYuSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShuYu
        fields = ['content']


class ParentLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryLesson
        fields = ('id','name','icon')

class LessonCategorySerializer(serializers.ModelSerializer):

    child = serializers.SerializerMethodField()

    class Meta:
        model = CategoryLesson
        fields = ('child',)
    def get_child(self,row):

        child_obj_list = row.Lessonchild.all().order_by('level')
        ret = []

        for item in child_obj_list:
            ret.append({'name':item.name,'id':item.id})
        return ret

class LessonChildSerializer(serializers.ModelSerializer):

    child  = serializers.SerializerMethodField()

    class Meta:
        model = CategoryLesson
        fields = ('id','name','icon','child')

    def get_child(self,row):

        child_obj_list = row.Lessonchild.all().order_by('level')
        ret = []

        for item in child_obj_list:
            ret.append({'name':item.name,'id':item.id})

        return ret

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('id','title','like','lessonimg')

class LessonContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('id','title','content','like')


class JSONWebTokenSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields['phone'] = serializers.CharField()
        self.fields['code'] = serializers.CharField()


    def validate(self, attrs):
        credentials = {
            'phone': attrs.get('phone'),
            'code': attrs.get('code'),
        }

        if all(credentials.values()):

            # 获取前端发送手机号和验证码
            phone = credentials['phone']
            code = credentials['code']

            # 获取 redis中用户的验证码
            sender = SmsSender()
            code_sender = sender.code_checker(phone)


            if code == code_sender:

                # 第一次登陆需要创建用户
                user,created = User.objects.get_or_create(phone=phone)

                #from rest_framework_jwt.settings import api_settings
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                #jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                #jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

                payload = jwt_payload_handler(user)

                #print(payload, jwt_encode_handler(payload), user,'=====')
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)

def jwt_payload_handler(user):
    #phone_field = 'phone'
    #phone = user.phone
    username_field = 'phone'
    username = user.phone

    payload = {
        'user_id': user.pk,
        'phone': username,
        'exp': datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    payload[username_field] = username


    return payload

