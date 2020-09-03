from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField #富文本编辑器
# Create your models here.


class GoodType(BaseModel):
    '''商品类型模型类'''
    name = models.CharField(max_length=20, verbose_name='种类名称') #verbose_name字段备注名
    logo = models.CharField(max_length=20, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSKU(BaseModel):
    '''商品SKull模型表'''
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    name = models.CharField(max_length = 20,verbose_name='商品名称')
    desc = models.CharField(max_length=256,verbose_name ='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length = 20,verbose_name='商品单位')
    stock = models.IntegerField(default=1,verbose_name='商品库存'),
    sales = models.IntegerField( default=0,verbose_name='商品销量'),
    imgs = models.ImageField(upload_to='goods', verbose_name='商品图片')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='商品状态')
    goods = models.ForeignKey('Goods',on_delete=models.CASCADE,verbose_name = '商品SPU')#多对一的关系
    type = models.ForeignKey('GoodType',on_delete=models.CASCADE,verbose_name='商品种类')

    class meta:
        db_table = 'df_good_sku' #数据库表名
        verbose_name = '商品'
        verbose_name_plural = verbose_name

class Goods(BaseModel):
    '''商品SPU模型乐'''
    name = models.CharField(max_length=20,verbose_name ='商品spu名称')
    #付文本类型，带有格斯的文本编辑起
    datail = HTMLField(blank=True,verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

class GoodsImage(BaseModel):
    '''商品图片模型类'''
    sku = models.ForeignKey('GoodsSKU',on_delete =models.CASCADE,verbose_name='sku_id')
    image =models.ImageField(upload_to='banner',verbose_name='图片')
    #but only allows values under a certain (database-dependent) point.
    index = models.SmallIntegerField(default=0, verbose_name='展示图片')

    class Meta:
        db_table ='df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

class IndexGoodBanner(BaseModel):
    '''首页轮播商品表'''
    sku_id = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE,verbose_name='商品')
    image = models.ImageField(upload_to='index_img',verbose_name='图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Mete:
        db_talbe = 'df_index_image'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

class IndexActivity(BaseModel):
    '''首页促销活动表'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    image = models.ImageField(upload_to='activity')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    url =models.URLField(verbose_name='活动链接')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "主页促销活动"
        verbose_name_plural = verbose_name

class IndexTypeGoodsBanner(BaseModel):
    '''首页分类商品展示模型类'''
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey('GoodType', verbose_name='商品类型',on_delete =models.CASCADE)
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU',on_delete =models.CASCADE)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name