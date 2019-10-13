from django.conf import settings
from django.core.mail import send_mail

from celery import Celery  # 导入celery包
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")  # 从wsgi.py中复制过来
django.setup()
# 创建一个Celery类的实例对象
# Celery(名称(一般写包名）, 中间人broke)
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/2')  # 2 使用第二个数据库




# 定义任务函数
@app.task  # 装饰 必不可少
def send_register_active_email(to_email, username, token):
    # '''发送激活邮件'''
    # 组织邮件信息
    # 发送邮件
    subject = '天天生鲜欢迎信息'  # 邮件主题
    # 邮件正文
    # 注：此处html标签是不会被解析出来 会当作字符串输出
    # message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户:<br/><a href="http://192.168.199.130:8000/user/active/%s">http://192.168.199.130:8000/user/active/%s</a>' % (username, token, token)
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 收件人列表
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://192.168.137.130:8000/user/active/%s">http://192.168.137.130:8000/user/active/%s</a>' % (
    username, token, token)
    print(html_message)
    # send_mail(邮件主题, 邮件正文, 发件人, 收件人列表, html_message=HTML格式的内容)
    # send_mail(subject, message, sender, receiver)
    send_mail(subject, message, sender, receiver, html_message=html_message)

# 生成静态首页
from django.template import loader, RequestContext  # templates包
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection
from django.core.cache import cache  # 导入缓存cache包
@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
    # 获取缓存数据
    context = cache.get('index_page_data')

    if context is None:
        print('设置缓存')
        # 获取商品的种类信息
        types = GoodsType.objects.all()

        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')

        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        # 获取首页分类商品展示信息
        for type in types:  # GoodsType
            # 获取type种类首页分类商品的图片展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
            # 获取type种类首页分类商品的文字展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

            # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
            type.image_banners = image_banners
            type.title_banners = title_banners

        # 组织模板上下文
        context = {'types': types,
                   'goods_banners': goods_banners,
                   'promotion_banners': promotion_banners}
        # 设置缓存
        # key  value timeout
        cache.set('index_page_data', context, 3600)

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')  # 需要导入templates包
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)
