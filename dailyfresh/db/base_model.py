from django.db import models
from datetime import date

class BaseModel(models.Model):
    '''模型抽象基类'''
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')  # auto_now_add= 创建时自动添加当前时间
    update_time = models.DateField(auto_now=True, verbose_name='修改时间')  # auto_now= 修改是自动添加当前时间
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明是一个抽象模型类
        abstract=True  # 没有这句会报错