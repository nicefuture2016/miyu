import django_filters

from api.models import ShuYu
from django.db.models import Q
import jieba,operator
from functools import reduce

from api.common.func import jieba_analyse

class ShuYuFilter(django_filters.rest_framework.FilterSet):

    girlsay = django_filters.CharFilter(field_name='girlsay', method='girl_say_filter')

    def girl_say_filter(self,queryset, field_name, value):
        query_match = []

        search_type = self.data.get('type')

        ret = jieba.lcut(value,cut_all=True)

        print(ret)
        # VIP搜索
        if search_type == 'vip':

            result = jieba_analyse(ret)

            query_match.append(Q(girlsay__icontains=value))

            for elment in result:

                query_match.append(Q(girlsay__icontains=elment))
        # 普通搜索
        else:

            # 小于两个字处理

            # 一个字处理
            if len(ret) == 1:
                query_match.append(Q(girlsay__icontains=ret[0]))

            # 两个单字处理

            elif len(ret) == 2 and len(ret[0]) == 1 and len(ret[1]) == 1:
                for word in ret:
                    query_match.append(Q(girlsay__icontains=word))

            # 多字组合处理
            else:
                for word in ret:
                    if len(word) >=2:
                        query_match.append(Q(girlsay__icontains=word))

        print(query_match)
        return queryset.filter(reduce(operator.or_, query_match))

    class Meta:
        model = ShuYu
        fields = ['girlsay']


