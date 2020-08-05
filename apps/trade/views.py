from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.utils.premissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .models import OrderGoods, OrderInfo, ShoppingCar
from .serializers import (ShoppingCarSerializer, ShoppingCarDetailSerializer,
                        OrderDetailSerializer, OrderSerializer)
# Create your views here.


class ShoppingCarViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车商品
    create：
        向购物车添加商品
    update:
        修改购物车信息
    delete:
        删除购物车商品
    """
    serializer_class = ShoppingCarSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, )
    lookup_field = "goods_id"

    def perform_create(self, serializer):
        shop_car = serializer.save()
        goods = shop_car.goods
        goods.goods_num -= shop_car.goods_num
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.goods_num
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCar.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.goods_num
        saved_record = serializer.save()
        nums = saved_record.goods_num - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCarDetailSerializer
        else:
            return ShoppingCarSerializer

    def get_queryset(self):
        return ShoppingCar.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取用户订单
    delete:
        删除订单
    create:
        添加订单
    """
    serializer_class = ShoppingCarSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, )

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_cars = ShoppingCar.objects.filter(user=self.request.user)
        for shopcar in shop_cars:
            order_goods = OrderGoods()
            order_goods.goods = shopcar.goods
            order_goods.goods_num = shopcar.nums
            order_goods.order = order
            order_goods.save()
        return order