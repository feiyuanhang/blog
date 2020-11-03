#-*- coding:utf-8 -*-
from django.template import Library

register = Library()


#定义一个将日的月份转换为大写的过滤器
@register.filter
def month_to_upper(key):
    return ['一','二','三','四','五','六','七','八','九','十','十一','十二'][key.month-1]
