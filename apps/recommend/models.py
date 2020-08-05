from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from goods.models import Goods, GoodsCategory
User = get_user_model()

# Create your models here.


class PopGoods(models.Model):
    """
    商品推荐
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目")

    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品推荐"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}:{1}".format(self.user.name, self.goods.name)

