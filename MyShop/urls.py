"""MyShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

import xadmin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from .settings import MEDIA_ROOT
from goods.views import (GoodsListViewset, GoodsCategoryViewset, BannerViewset,
                         IndexCategoryViewset, BrandViewset)
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavinfMessageViewset, UserAddressViewset
from trade.views import ShoppingCarViewset, OrderViewset
from recommend.views import RecommendViewset

router = DefaultRouter()

router.register("goods", GoodsListViewset, basename="goods")
router.register("categorys", GoodsCategoryViewset, basename="categorys")
router.register("codes", SmsCodeViewset, basename="codes")
router.register("users", UserViewset, basename="users")
router.register("usersfav", UserFavViewset, basename="usersfav")
router.register("message", LeavinfMessageViewset, basename="message")
router.register("address", UserAddressViewset, basename="address")
router.register("shopcar", ShoppingCarViewset, basename="shopcar")
router.register("orders", OrderViewset, basename="orders")
router.register("banners", BannerViewset, basename="banners")
router.register("indexgoods", IndexCategoryViewset, basename="indexgoods")
router.register("brands", BrandViewset, basename="brands")
router.register("recommend", RecommendViewset, basename="recommend")

urlpatterns = [
       path('admin/', xadmin.site.urls),
       path('api_auth/', include("rest_framework.urls", namespace="rest_framework")),
       path('', include(router.urls)),
       path('index/', TemplateView.as_view(template_name="index.html"), name="index"),
       re_path('media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

       path('api-token-auth/', views.obtain_auth_token),
       path('login/', obtain_jwt_token),
       path('ueditor', include('DjangoUeditor.urls')),
       path('doc/', include_docs_urls(title="商城")),



]
