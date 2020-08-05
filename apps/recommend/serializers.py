# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from rest_framework import serializers

from .models import PopGoods


class RecommendGoodsSerializer(serializers.ModelSerializer):
    """
    推广商品
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PopGoods
        fields = "__all__"