#!/usr/bin/env python
# encoding: utf-8
import xadmin
from .models import PopGoods


class PopGoodsAdmin(object):
    list_display = ['user', 'goods', "category","add_time"]



xadmin.site.register(PopGoods, PopGoodsAdmin)


