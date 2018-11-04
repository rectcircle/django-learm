# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializrse define the API representation.
# 序列化配置：针对的模型是User，需要返回的信息在fields中声明
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
# 定义视图行为：首先定义数据库查询的方式，然后指定序列化器
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
# 路由规则
router = routers.DefaultRouter()
router.register(r'users', UserViewSet) # 将url与视图集绑定

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
