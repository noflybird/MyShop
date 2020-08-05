from django.db import models
from django.utils import timezone

from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(models.Model):
    """
    商品种类model
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目")
    )
    name = models.CharField(max_length=30, default="", verbose_name="类别名", help_text="类别名")
    code = models.CharField(max_length=30, default="", verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name="父类目",help_text="父目录", related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="brands", verbose_name="商品类目")
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = UEditorField(verbose_name=u"品牌描述", imagePath="brand/images/", width=1000,
                              height=300, filePath="brand/files/", default="在此填写品牌描述")
    hot_brand = models.BooleanField(default=False, verbose_name="是否热门")
    image = models.ImageField(upload_to="brand/", max_length=200)
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "品牌名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品model
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name="商品类目")
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品统一货号")
    name = models.CharField(max_length=300, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="销量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    sale_price = models.FloatField(default=0.0, verbose_name="售价")
    discount_price = models.FloatField(default=0.0, verbose_name="折扣价")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简介")
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000,
                              height=300, filePath="goods/files/", default="在此填写商品描述")
    deliver_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    is_pop = models.BooleanField(default=False, verbose_name="是否推广")

    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="goods/images/", verbose_name="图片", null=True, blank=True)
    image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name="图片url")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    image = models.ImageField(upload_to="banner", verbose_name="轮播图片")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE,  verbose_name="商品类目", related_name="category")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="goods")

    class Meta:
        verbose_name = "首页商品类别广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


