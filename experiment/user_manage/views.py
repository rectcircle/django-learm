# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics, mixins, viewsets
from rest_framework.templatetags import rest_framework

from dongtai import message
from user_manage.models import Student
from user_manage.serializers import StudentSerializer, UserSerializer
from user_manage.utils import WrapResponse, need_login, wrap_response


### 使用函数返回视图 ###

# @login_required
@need_login
def need_login_view(request):
    """测试登录校验"""
    return JsonResponse({'message': request.user.username})

def hello(request):
    """测试返回数据"""
    return JsonResponse({'message':'hello!',})

def middleware(request):
    """测试middleware"""
    return JsonResponse({'POST': request.POST, 'GET':request.GET, 'DATA':request.DATA})

def login(request):
    username = request.DATA.get('username')
    password = request.DATA.get('password')
    result = auth.authenticate(username=username, password=password)
    if result is None:
        return JsonResponse({'message': 'username or password error'}, status=400)
    auth.login(request, result)  # 登陆成功
    return JsonResponse({'message': 'success'}, status=200)

def logout(request):
    auth.logout(request)
    return JsonResponse({'message': 'success'}, status=200)

### 对象返回视图 ###

class CreateStudentView(mixins.CreateModelMixin, generics.GenericAPIView):
# class CreateStudentView(generics.CreateAPIView): # 与上方写法等价
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return JsonResponse({'message': 'success'}, status=201)


    def perform_create(self, serializer):
        userSerializer = UserSerializer(data=self.request.data)
        print self.request.data
        if userSerializer.is_valid():
            serializer.save(user=userSerializer.save())

@wrap_response
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # 以下为常用的覆写方法：

    # 来自mixins.CreateModelMixin
    # 将影响POST（insert）行为
    def perform_create(self, serializer):
        return super(StudentViewSet, self).perform_create(serializer)

    # 来自mixins.RetrieveModelMixin
    # 将影响GET（get one）方法
    def retrieve(self, request, *args, **kwargs):
        return super(StudentViewSet, self).retrieve(request, *args, **kwargs)

    # 来自mixins.UpdateModelMixin
    # 将影响PUT（更新全部）方法
    def perform_update(self, serializer):
        return super(StudentViewSet, self).perform_update(serializer)

    # 来自mixins.UpdateModelMixin
    # 将影响patch（更新部分）方法
    def partial_update(self, request, *args, **kwargs):
        return super(StudentViewSet, self).partial_update(request, *args, **kwargs)

    # 来自mixins.DestroyModelMixin
    # 将影响delete（更新部分）方法
    def perform_destroy(self, instance):
        return super(StudentViewSet, self).perform_destroy(instance)

    # 来自mixins.ListModelMixin
    # 将影响GET（get list）方法
    def list(self, request, *args, **kwargs):
        return super(StudentViewSet, self).list(request, *args, **kwargs)
