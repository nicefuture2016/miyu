from rest_framework.throttling import SimpleRateThrottle

class DefaultThrottle(SimpleRateThrottle):

    # 200/d
    scope = 'default'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class DataThrottle(SimpleRateThrottle):
    # 10/m
    scope = 'data'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

