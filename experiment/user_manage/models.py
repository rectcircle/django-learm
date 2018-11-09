# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Student(models.Model):

    objects = models.Manager()

    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "Student(name={}, class_name={})".format(self.name, self.class_name)

