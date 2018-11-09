# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin


class RequestEnhanceMiddleware(MiddlewareMixin):
    """Request增强
    1. 创建DATA字段：存放POST和GET的并集
    """
    
    def process_request(self, request):
        request.DATA = request.GET.copy()
        request.DATA.update(request.POST)
