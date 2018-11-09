# -*- coding: utf-8 -*-

import logging
import types
from collections import OrderedDict
from types import MethodType

from django.http import JsonResponse
from django.utils.decorators import classonlymethod
from rest_framework.response import Response
from rest_framework.views import APIView


def need_login(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({'message':'need login'}, status=401)
        return func(request, *args, **kwargs)
    return wrapper

def get_request_data(request):
    """从request中获取get和post的数据的集合"""
    data = request.GET.copy()
    data.update(request.POST)
    return data


def _return_wrapper_response_as_view(as_view):
    def wrapper(request, *args, **kwargs):
        response = as_view(request, *args, **kwargs)
        print type(response)
        if isinstance(response, Response) and response.accepted_media_type == u'application/json':
            response.data = OrderedDict(
                code=0, msg='success', data=response.data)
            return response
        return response
    return wrapper

class WrapResponse(APIView):

    @classmethod
    def as_view(cls, *args, **initkwargs):
        # 返回一个函数 该函数 为 request -> HttpResponse
        handle = super(WrapResponse, cls).as_view(*args, **initkwargs)
        return _return_wrapper_response_as_view(handle)

# def wrap_response(wrap_class):
#     # http://python.jobbole.com/85939/
#     print "+++++++++++"
#     print wrap_class.as_view 
#     print wrap_class.list
#     class NewClass(wrap_class):
#         @classmethod
#         def as_view(cls, *args, **initkwargs):
#             # 返回一个函数 该函数 为 request -> HttpResponse
#             handle = super(NewClass, cls).as_view(*args, **initkwargs)
#             return _return_wrapper_response_as_view(handle)
#     return NewClass


def wrap_response(wrap_class):
    # http://python.jobbole.com/85939/
    print "+++++++++++"
    print wrap_class.as_view
    print wrap_class.list

    old_as_view = wrap_class.as_view

    def as_view(cls, *args, **initkwargs):
        # 返回一个函数 该函数 为 request -> HttpResponse
        handle = old_as_view(*args, **initkwargs)
        return _return_wrapper_response_as_view(handle)

    wrap_class.as_view = types.MethodType(as_view, wrap_class)
    print wrap_class.as_view

    return wrap_class
