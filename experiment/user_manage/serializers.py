# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user_manage import models


# Json结构化返回数据写法
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {
                'required': True,
            },
            'password': {
                'write_only': True, 
                'required': True, 
            },
        }
    def validate(self, attrs):
        print "--------------------"
        if User.objects.filter(username=attrs['username']).count() != 0:
            raise serializers.ValidationError('用户已注册')
        return attrs

    def validate_password(self, password):
        print "==================="
        return make_password(password)


# class StudentSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = models.Student
#         fields = ('name', 'class_name', 'user')

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    class Meta:
        model = models.Student
        fields = ('username', 'password', 'name', 'class_name',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, },
        }

    # 对应insert
    def create(self, validated_data):
        return super(StudentSerializer, self).create(validated_data)
    # 对应update
    def update(self, instance, validated_data):
        return super(StudentSerializer, self).update(instance, validated_data)
    # 对应updateOrinsert
    def save(self, **kwargs):
        return super(StudentSerializer, self).save(**kwargs)
    
class FieldTestSerializer(serializers.Serializer):
    read_field = serializers.CharField(read_only=True)
    write_field = serializers.CharField(write_only=True)
    normal_field =serializers.CharField()