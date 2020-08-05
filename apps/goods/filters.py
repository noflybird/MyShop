# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
import django_filters as dfs
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品过滤器
    """
    pricemin = dfs.NumberFilter(field_name="discount_price", lookup_expr="gte")
    pricemax = dfs.NumberFilter(field_name="discount_price", lookup_expr="lte")
    # 过滤商品类别
    top_category = dfs.NumberFilter(method="top_category_filter")

    def top_category_filter(self, queryset, name,value):
        return queryset.filter(Q(category_id=value) |
                               Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ["pricemin", "pricemax", "is_hot", "is_new"]
