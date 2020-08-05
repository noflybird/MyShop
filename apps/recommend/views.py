from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.permissions import IsAuthenticated

from utils.premissions import IsOwnerOrReadOnly
from  .models import PopGoods
from .serializers import RecommendGoodsSerializer
# Create your views here.


class RecommendViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户商品推荐
        list:推荐列表
    """
    queryset = PopGoods.objects.all().order_by("-add_time")
    serializer_class = RecommendGoodsSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

