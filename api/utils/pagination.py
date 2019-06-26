from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param
class MyPageNumberPagination(PageNumberPagination):

    '''
    分页类
    '''
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 10
    page_query_param = 'page'

    def get_next_link(self):
        '''
        获取下一页
        :return:
        '''
        if not self.page.has_next():
            return None
        return self.page.number + 1

    def get_previous_link(self):
        '''
        获取上一页
        :return:
        '''
        if not self.page.has_previous():
            return None
        return self.page.number - 1

    def get_paginated_response(self, data):
        '''
        返回自定义数据
        :param data:
        :return:
        '''
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))