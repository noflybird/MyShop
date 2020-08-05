from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner, IndexAd, GoodsCategoryBrand
from goods.serializers import (GoodsSerializer, CategorySerializer1, BannerSerializer,
                               IndexCategorySerializer, BrandDetailSerializer)
from goods.filters import GoodsFilter
# Create your views here.


class GoodsPageination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin ,viewsets.GenericViewSet):
    """
    商品
    list:
        获取商品

    """
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer
    pagination_class = GoodsPageination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_class = GoodsFilter

    search_fields = ("name", "goods_brief", "goods_desc")
    ordering_fields = ("sold_num", "add_time")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品类目
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer1


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("id")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer


class BrandViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    品牌主页
    """
    queryset = GoodsCategoryBrand.objects.all().order_by("id")
    serializer_class = BrandDetailSerializer

    filter_backends = (filters.SearchFilter,)

    search_fields = ("name", "desc")



