from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse  # 反响解析
from django.views.generic import View  # 导入类试图
from django.conf import settings  # 导入配置文件 获取私钥
from django.core.mail import send_mail  # 导入发送邮件的包


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # 导入itsdangerous里面的类 实现加密
import re

from celery_tasks.tasks import send_register_active_email  # 导入celery发邮件的方法
from user.models import *
# Create your views here.

class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 校验
        # 数据完整度
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 邮箱验证
        if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 校验协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户是否存在
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            user = None
        if user:
            # 用户已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行用户注册
        # create_user() 注册用户
        user = User.objects.create_user(username, email, password)
        user.is_active = 0  # 0为未激活状态
        user.save()

        # 进行token加密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info).decode('utf-8')

        # 发送邮件
        # delay(收件人, 用户名, token)
        send_register_active_email.delay(email, username, token)  # 把任务放入队列


        # subject = '天天生鲜欢迎信息'  # 邮件主题
        # # 邮件正文
        # # 注：此处html标签是不会被解析出来 会当作字符串输出
        # # message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户:<br/><a href="http://192.168.199.130:8000/user/active/%s">http://192.168.199.130:8000/user/active/%s</a>' % (username, token, token)
        # message = ''
        # sender = settings.EMAIL_FROM  # 发件人
        # receiver = [email]  # 收件人列表
        # html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://192.168.199.130:8000/user/active/%s">http://192.168.199.130:8000/user/active/%s</a>' % (username, token, token)
        # print(html_message)
        # # send_mail(邮件主题, 邮件正文, 发件人, 收件人列表, html_message=HTML格式的内容)
        # # send_mail(subject, message, sender, receiver)
        # send_mail(subject, message, sender, receiver, html_message=html_message)

        return redirect(reverse('goods:index'))

# 用户激活
from itsdangerous import SignatureExpired  # 解密信息过期错误
class ActiveView(View):
    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密 获取要激活的用户信息
        print(token)
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)

            # 获取待激活用户id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')


# 登录
from django.contrib.auth import authenticate, login  # authenticate:user认证  login:用户登录并记录session
class LoginView(View):
    '''登录'''
    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username= ''
            checked = ''
        # 使用模板
        return render(request, 'login.html', {'checked':checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # print(username)
        # print(password)

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})

        user = authenticate(username=username, password=password)  # 查找数据库，有的话返回user信息 没有的话返回None
        print(user.password)
        if user is not None:
            # 用户名和密码正确
            # 验证是否激活
            if user.is_active:
                # 用户已激活
                # 记录用户登录状态
                # print(user.is_active)
                flag = login(request, user)  # django.contrib.auth中的login方法
                # 跳转到首页
                # response = redirect(reverse('goods:index'))  # HttpResponseRedirct

                # 接收当前访问的地址
                next_url = request.GET.get('next', reverse('goods:index'))  # get() 第二个参数设置默认地址
                # 登录校验 如果登录了 跳转到先前访问的地址
                response = redirect(next_url)
                # 判断是否要记住用户名
                remember = request.POST.get('remember')
                print(remember)
                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)  # 记录cookie
                else:
                    response.delete_cookie('username')
                # 返回response
                return response

            else:
                return render(request, 'login.html', {'errmsg':'用户尚未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg':'用户名或密码错误'})


# 退出
from django.contrib.auth import logout  # logout:退出并清除session信息
class LogoutView(View):
    def get(self, request):
        '''退出页面'''
        # 退出并清除session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))


from utils.mixin import LoginRequiredMinxin
# 用户信息中心
# /user
class UserInfoView(LoginRequiredMinxin, View):
    def get(self, request):
        '''显示用户信息页面'''
        # Django会给request对象添加一个属性request.user
        # 如果用户未登录->user是AnonymousUser类的一个实例对象
        # 如果用户登录->user是User类的一个实例对象
        # request.user.is_authenticated()
        # 除了你给模板文件传递的模板变量以外，django框架会把request.user也传递给模板文件

        # 显示个人信息
        user = request.user
        address = Address.objects.get_default_addr(user)

        # 获取历史记录
        from django_redis import get_redis_connection
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)
        # 从数据库中查询用户浏览的商品的具体信息
        from goods.models import GoodsSKU
        # 方法1
        # goods_ids = GoodsSKU.objects.get(id__in=sku_ids)
        # goods_list = []
        # for s_id in sku_ids:
        #     for goods in goods_ids:
        #         if s_id == goods.id:
        #             goods_list.append(goods)
        # 方法2
        goods_li = []
        # 根据redis取出的列表的id顺序查询出商品 遍历出来
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 组织上下文
        context = {
            'address': address,
            'page': 'user',
            'goods_li':goods_li
        }
        return render(request, 'user_center_info.html', context)


# 用户订单中心
# /user/order
class UserOrderView(LoginRequiredMinxin, View):
    def get(self, request):
        '''显示用户信息页面'''
        from fdfs_client.client import Fdfs_client
        # client = Fdfs_client('/etc/fdfs/client.conf')
        # ret = client.upload_by_filename('test')
        # print(ret)
        return render(request, 'user_center_order.html', {'page':'order'})


# 用户地址
# /user/address
from user.models import Address
class AddressView(LoginRequiredMinxin, View):
    def get(self, request):
        '''显示用户信息页面'''
        # 获取地址信息
        user = request.user
        address = Address.objects.get_default_addr(user)
        print(address)
        return render(request, 'user_center_site.html', {'page':'address', 'address':address})

    def post(self, request):
        '''添加地址'''
        # 接收数据
        receiver = request.POST.get('receiver')
        zip_code = request.POST.get('zip_code')
        addr = request.POST.get('addr')
        phone = request.POST.get('phone')
        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg':'手机格式不正确'})
        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user
        address = Address.objects.get_default_addr(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               zip_code=zip_code,
                               addr=addr,
                               phone=phone,
                               is_default=is_default)
        # 返回应答 刷新页面
        return redirect(reverse('user:address'))