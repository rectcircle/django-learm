"""experiment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import views
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from user_manage.utils import WrapResponse, need_login, wrap_response
from user_manage.views import StudentViewSet


router = DefaultRouter()
print "=========="
router.register(r'student', StudentViewSet)


urlpatterns = [
    url(r'^$', views.hello),
    url(r'^need_login$', views.need_login_view),
    url(r'^middleware$', views.middleware),
    url(r'^login', views.login),
    url(r'^student/register', views.CreateStudentView.as_view()),
    url(r'^', include(router.urls))
]
