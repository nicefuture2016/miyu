from django.http.response import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from api.models import CategoryParent,CategoryChild,ShuYu,CategoryLesson,CategoryLessonChild,Lesson
from .forms import LoginForm,ShuyuForm,ArticleForm

def sys_login(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST or None)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            error_msg = '用户名或密码错误'
            return render(request, "login.html", {"error_msg": error_msg,'login_form':login_form})
    else:
        login_form = LoginForm()
    return render(request,'login.html',locals())

@login_required
def sys_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("sys_login"))

@login_required
def index(request):
    parent = CategoryParent.objects.all().order_by('level')

    return render(request,'index.html',locals())

@login_required
def sys_child(request,pid,cid):

    shuyu = CategoryChild.objects.get(pk=cid).shuyu.all()
    return render(request,'sys_child.html',locals())

@login_required
def sys_shuyu_add(request):

    if request.method == 'POST':
        form = ShuyuForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            msg = '添加成功'
        else:
            error = '添加失败'
    else:
        form = ShuyuForm()
        print(form)

    return render(request, 'sys_shuyu_add.html', locals())

@login_required
def sys_shuyu_edit(request, pk):

    shuyu_obj = ShuYu.objects.get(pk=pk)
    if request.method == 'POST':
        form = ShuyuForm(request.POST, instance=shuyu_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            msg = '修改成功'
        else:
            error = '修改失败'
    else:
        form = ShuyuForm(instance=shuyu_obj)

    return render(request, 'sys_shuyu_edit.html', locals())


@login_required
def article(request):
    article = CategoryLesson.objects.all().order_by('level')

    return render(request,'article.html',locals())

@login_required
def sys_lesson_child(request,pid,cid):
    parent = CategoryLesson.objects.get(pk=pid)
    child = CategoryLessonChild.objects.get(pk=cid)
    article = child.lesson.all()
    return render(request,'sys_lesson.html',locals())


@login_required
def sys_article_add(request,pk):

    child = CategoryLessonChild.objects.get(pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            lesson = Lesson.objects.filter(title=form.cleaned_data.get('title'),lessonimg=form.cleaned_data.get('lessonimg'))
            child.lesson.add(*lesson)
            msg = '添加成功'
        else:
            error = '添加失败'
    else:
        form = ArticleForm()


    return render(request, 'sys_article_add.html', locals())

@login_required
def sys_article_edit(request, pk):

    print(pk)
    article_obj = Lesson.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            msg = '修改成功'
        else:
            error = '修改失败'
    else:
        form = ArticleForm(instance=article_obj)

    return render(request, 'sys_article_edit.html', locals())


@login_required
def delarticle(request):

    ret = {'code':10000,'msg':'删除成功'}

    pk = request.POST.get('pk')

    try:
        Lesson.objects.get(pk=pk).delete()
    except Exception as e:
        ret['msg'] = '删除失败'
        ret['code'] = 10001

    return JsonResponse(ret)