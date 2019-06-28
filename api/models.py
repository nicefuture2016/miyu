from django.db import models

ROLE = (
    (1, "普通用户"),
    (2, "SVIP用户")
)

# 主页推荐分类
CATEGORY_MAIN = (
    (1, "显示"),
    (2, "不显示")
)

class Log(models.Model):
    logid = models.CharField(db_column='logId', primary_key=True, max_length=45)  # Field name made lowercase.
    log = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'


class TblArticle(models.Model):
    articleid = models.CharField(db_column='articleId', primary_key=True, max_length=45)  # Field name made lowercase.
    articletitle = models.CharField(db_column='articleTitle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    articlewriter = models.CharField(db_column='articleWriter', max_length=45, blank=True, null=True)  # Field name made lowercase.
    articleimg = models.CharField(db_column='articleImg', max_length=200, blank=True, null=True)  # Field name made lowercase.
    articledate = models.DateTimeField(db_column='articleDate', blank=True, null=True)  # Field name made lowercase.
    articlecontent = models.TextField(db_column='articleContent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_article'


class TblCategory(models.Model):
    categoryid = models.CharField(db_column='categoryId', primary_key=True, max_length=45)  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    categorylevel = models.CharField(db_column='categoryLevel', max_length=45, blank=True, null=True)  # Field name made lowercase.
    parentid = models.CharField(db_column='parentId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    categorysort = models.IntegerField(db_column='categorySort', blank=True, null=True)  # Field name made lowercase.
    categorytype = models.CharField(db_column='categoryType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    materialurl = models.CharField(db_column='materialUrl', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_category'


class TblChat(models.Model):
    chatid = models.CharField(db_column='chatId', primary_key=True, max_length=45)  # Field name made lowercase.
    category1 = models.CharField(max_length=45, blank=True, null=True)
    category2 = models.CharField(max_length=45, blank=True, null=True)
    chatcontent = models.TextField(db_column='chatContent', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_chat'

class ShuYu(models.Model):
    content = models.TextField(blank=True, null=True)
    girlsay = models.CharField(max_length=500,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content
    class Meta:
        db_table = 'shuyu'

class CategoryChild(models.Model):
    name = models.CharField(max_length=45,blank=True, null=True)
    shuyu = models.ManyToManyField(ShuYu, blank=True)

    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'categorychild'

class CategoryParent(models.Model):
    name = models.CharField(max_length=45,blank=True, null=True)
    info = models.CharField(max_length=45, blank=True, null=True)
    level = models.SmallIntegerField(default=1)
    child = models.ManyToManyField(CategoryChild, blank=True)


    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'categoryparent'

class Lesson(models.Model):
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    lessonimg = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.SmallIntegerField(default=1050)
    def __unicode__(self):
        return self.title
    class Meta:
        db_table = 'lesson'


class CategoryLessonChild(models.Model):

    name = models.CharField(max_length=45, blank=True, null=True)
    lesson = models.ManyToManyField(Lesson)
    level = models.SmallIntegerField(default=1)
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'categorylessonchild'

class CategoryLesson(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    icon = models.CharField(max_length=300, blank=True, null=True)
    Lessonchild = models.ManyToManyField(CategoryLessonChild)
    level = models.SmallIntegerField(default=1)
    role = models.IntegerField(choices=CATEGORY_MAIN, default=2)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'categorylesson'


class User(models.Model):
    phone = models.CharField(max_length=45,unique=True)
    role =  models.IntegerField(choices=ROLE,default=1)
    score = models.IntegerField(default=10)
    token = models.CharField(max_length=64,blank=True, null=True)
    lesson = models.ManyToManyField(Lesson)
    class Meta:
        db_table = 'user'

class TblDictionary(models.Model):
    dictionaryid = models.CharField(db_column='dictionaryId', primary_key=True, max_length=45)  # Field name made lowercase.
    d_key = models.CharField(max_length=45, blank=True, null=True)
    d_value = models.CharField(max_length=45, blank=True, null=True)
    remark = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_dictionary'


class TblEssay(models.Model):
    essayid = models.CharField(db_column='essayId', primary_key=True, max_length=45)  # Field name made lowercase.
    essaynum = models.CharField(db_column='essayNum', max_length=45, blank=True, null=True)  # Field name made lowercase.
    essaytype = models.CharField(db_column='essayType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    essaytitle = models.CharField(db_column='essayTitle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    essaycontent = models.TextField(db_column='essayContent', blank=True, null=True)  # Field name made lowercase.
    essayimg = models.CharField(db_column='essayImg', max_length=200, blank=True, null=True)  # Field name made lowercase.
    essaywriter = models.CharField(db_column='essayWriter', max_length=45, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    video = models.CharField(max_length=500, blank=True, null=True)
    audio = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_essay'


class TblEssayType(models.Model):
    etid = models.CharField(db_column='etId', primary_key=True, max_length=45)  # Field name made lowercase.
    etname = models.CharField(db_column='etName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    eticon = models.CharField(db_column='etIcon', max_length=200, blank=True, null=True)  # Field name made lowercase.
    etsort = models.IntegerField(db_column='etSort', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_essay_type'


class TblMaterial(models.Model):
    materialid = models.CharField(db_column='materialId', primary_key=True, max_length=45)  # Field name made lowercase.
    materialname = models.CharField(db_column='materialName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    materialwriter = models.CharField(db_column='materialWriter', max_length=45, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    materialcontent = models.TextField(db_column='materialContent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_material'


class TblOrder(models.Model):
    orderid = models.CharField(db_column='orderId', primary_key=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_order'


class TblPraise(models.Model):
    praiseid = models.CharField(db_column='praiseId', primary_key=True, max_length=45)  # Field name made lowercase.
    qaid = models.CharField(db_column='qaId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    openid = models.CharField(db_column='openId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    praisedate = models.DateTimeField(db_column='praiseDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_praise'


class TblQa(models.Model):
    qaid = models.CharField(db_column='qaId', primary_key=True, max_length=45)  # Field name made lowercase.
    qatitle = models.CharField(db_column='qaTitle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qaimg = models.CharField(db_column='qaImg', max_length=200, blank=True, null=True)  # Field name made lowercase.
    qacontent = models.TextField(db_column='qaContent', blank=True, null=True)  # Field name made lowercase.
    createrid = models.CharField(db_column='createrId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    creatername = models.CharField(db_column='createrName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    createricon = models.CharField(db_column='createrIcon', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=45, blank=True, null=True)
    praise = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_qa'


class TblReply(models.Model):
    replyid = models.CharField(db_column='replyId', primary_key=True, max_length=45)  # Field name made lowercase.
    qaid = models.CharField(db_column='qaId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    reply = models.TextField(blank=True, null=True)
    replydate = models.DateTimeField(db_column='replyDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_reply'


class TblSearch(models.Model):
    searchid = models.CharField(db_column='searchId', primary_key=True, max_length=45)  # Field name made lowercase.
    searchdate = models.DateTimeField(db_column='searchDate')  # Field name made lowercase.
    searchword = models.CharField(db_column='searchWord', max_length=45, blank=True, null=True)  # Field name made lowercase.
    searchcount = models.IntegerField(db_column='searchCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_search'


class TblUser(models.Model):
    a_username = models.CharField(primary_key=True, max_length=45)
    a_password = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user'


class TblWechat(models.Model):
    openid = models.CharField(db_column='openId', primary_key=True, max_length=45)  # Field name made lowercase.
    nickname = models.CharField(db_column='nickName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(max_length=200, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    searchdate = models.DateField(db_column='searchDate', blank=True, null=True)  # Field name made lowercase.
    membertype = models.CharField(db_column='memberType', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_wechat'
