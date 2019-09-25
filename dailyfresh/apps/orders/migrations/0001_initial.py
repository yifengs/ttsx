# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('create_time', models.DateField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateField(verbose_name='修改时间', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('comment', models.CharField(verbose_name='评论', max_length=256)),
            ],
            options={
                'verbose_name_plural': '订单商品',
                'verbose_name': '订单商品',
                'db_table': 'df_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateField(verbose_name='修改时间', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('order_id', models.CharField(primary_key=True, verbose_name='订单id', max_length=128, serialize=False)),
                ('pay_method', models.SmallIntegerField(default=3, verbose_name='支付方式', choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')])),
                ('total_count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('total_price', models.DecimalField(verbose_name='商品总价', decimal_places=2, max_digits=10)),
                ('transit_price', models.DecimalField(verbose_name='订单运费', decimal_places=2, max_digits=10)),
                ('order_status', models.SmallIntegerField(default=1, verbose_name='订单状态', choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')])),
                ('trade_no', models.CharField(verbose_name='支付编号', max_length=128)),
            ],
            options={
                'verbose_name_plural': '订单',
                'verbose_name': '订单',
                'db_table': 'df_order_info',
            },
        ),
    ]
