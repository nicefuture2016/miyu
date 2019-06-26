from django.contrib import admin

from .models import TblCategory,TblChat,CategoryParent,CategoryChild,ShuYu,CategoryLesson,CategoryLessonChild
# Register your models here.


class TblCategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryid','categoryname','categorylevel','parentid','categorysort','categorytype')
admin.site.register(TblCategory, TblCategoryAdmin)

class TblChatAdmin(admin.ModelAdmin):
    list_display = ('chatid','category1','category2','chatcontent','createdate')
    search_fields = ('chatid', 'category1', 'category2','createdate')
admin.site.register(TblChat, TblChatAdmin)


class CategoryParentAdmin(admin.ModelAdmin):
    list_display = ('name','info')
admin.site.register(CategoryParent, CategoryParentAdmin)


class CategoryChildAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(CategoryChild, CategoryChildAdmin)

class ShuYuAdmin(admin.ModelAdmin):
    list_display = ('content','created','updated',)
    search_fields = ('content',)
admin.site.register(ShuYu, ShuYuAdmin)


class CategoryLessonAdmin(admin.ModelAdmin):
    list_display = ('name','icon','level',)
admin.site.register(CategoryLesson, CategoryLessonAdmin)

class CategoryLessonChildAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(CategoryLessonChild, CategoryLessonChildAdmin)