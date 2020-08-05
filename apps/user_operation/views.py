from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import (UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer,
                            UserAddressSerializer)
from .models import UserFav, UserAddress, UserLeavingMessage
from utils.premissions import IsOwnerOrReadOnly

# Create your views here.


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏
    retrieve:
        判断用户是否收藏
    delete:
        取消收藏
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, )
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user, )

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer


class LeavinfMessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    delete:
        删除留言
    create:
        添加留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, )

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewset(viewsets.ModelViewSet):
    """
    list:
        获取地址信息
    create:
        添加地址信息
    delete:
        删除地址信息
    update:
        修改地址信息
    """
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, )

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)