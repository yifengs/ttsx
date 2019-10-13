from django.contrib import admin
from goods.models import *

# Register your models here.
from django.core.cache import cache
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或修改的时候调用'''
        # 调用父类的save_model()方法
        super().save_model(request, obj, form, change)
        # 调用celery重新生成
        from celery_tasks.tasks import generate_static_index_html  # 不能放在上面 不然会报错
        generate_static_index_html.delay()
        # 清除首页缓存数据
        cache.delete('index_page_data')


    def delete_model(self, request, obj):
        '''删除数据时候调用'''
        # 调用父类delete_model()方法
        super().delete_model(request, obj)
        # 重新生成静态页面
        from celery_tasks.tasks import generate_static_index_html  # 不能放在上面 不然会报错
        generate_static_index_html.delay()
        # 清除首页缓存数据
        cache.delete('index_page_data')

class IndexPromotionAdmin(BaseModelAdmin):
    pass

class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass

class GoodsTypeAdmin(BaseModelAdmin):
    pass

class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass

class GoodsSkuAdmin(BaseModelAdmin):
    pass

admin.site.register(GoodsSKU, GoodsSkuAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
