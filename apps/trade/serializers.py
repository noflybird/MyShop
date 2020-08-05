# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
import time
from random import Random, choice

from rest_framework import serializers

from .models import ShoppingCar, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from goods.models import Goods


class ShoppingCarDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCar
        fields = ("goods", "goods_num")


class ShoppingCarSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    goods_num = serializers.IntegerField(required=True, min_value=1,
                                         error_messages={
                                             "min_value": "商品数不能小于1",
                                             "required": "请选择购买数量"
                                         })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        goods_nums = validated_data["goods_num"]
        goods = validated_data["goods"]
        existed = ShoppingCar.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.goods_num += goods_nums
            existed.save()
        else:
            existed = ShoppingCar.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_sn = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)

    add_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def generate_trade_sn(self):
        random_strs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        random_str = []
        for i in range(20):
            random_str.append(choice(random_strs))
        trade_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr="".join(random_str))

        return trade_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        attrs["trade_sn"] = self.generate_trade_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
