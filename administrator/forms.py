#-*- coding:utf-8 -*-
from api.models import ShuYu,Lesson
from django.forms import widgets as Fwidgets
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "用户名"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}),
        error_messages={'error_messages': '用户或密码错误'}
    )
    #username = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "用户名"}),
    #password = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}),
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class ShuyuForm(forms.ModelForm):
    class Meta:
        model = ShuYu
        fields = ['content','girlsay',]

        labels = {
            'content': '术语内容',
            'girlsay': '女孩说的话',
        }
        widgets = {
            'content': SummernoteWidget(),
            'girlsay': Fwidgets.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ShuyuForm, self).__init__(*args, **kwargs)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','content','lessonimg','like']

        labels = {
            'title': '文章标题',
            'content': '文章内容',
            'lessonimg': '预览图片',
            'like': '点赞数'
        }
        widgets = {
            'title': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(),
            'lessonimg': Fwidgets.TextInput(attrs={'class': 'form-control'}),
            'like': Fwidgets.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)