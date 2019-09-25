from django.conf import settings
from django.core.mail import send_mail

from celery import Celery  # 导入celery包
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")  # 从wsgi.py中复制过来
django.setup()
# 创建一个Celery类的实例对象
# Celery(名称(一般写包名）, 中间人broke)
app = Celery('celery_tasks.tasks', broker='redis://192.168.199.130:6379/2')  # 2 使用第二个数据库




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
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://192.168.199.130:8000/user/active/%s">http://192.168.199.130:8000/user/active/%s</a>' % (
    username, token, token)
    print(html_message)
    # send_mail(邮件主题, 邮件正文, 发件人, 收件人列表, html_message=HTML格式的内容)
    # send_mail(subject, message, sender, receiver)
    send_mail(subject, message, sender, receiver, html_message=html_message)