# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pygments import highlight


from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from django.db.models import Manager

# Create your models here.

# 获取到词法法解析器
LEXERS = [item for item in get_all_lexers() if item[1]]
# 获取到语言类型
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# 获取到样式风格
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    """代码片段模型"""
    created = models.DateTimeField(auto_now_add=True) # 创建时间
    title = models.CharField(max_length=100, blank=True, default='') # 标题
    code = models.TextField() # 代码文本
    linenos = models.BooleanField(default=False) # 
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python', max_length=100) # 语言选择
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly', max_length=100) # 配色样式
    owner = models.ForeignKey(
        'auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    # objects = Manager()

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)