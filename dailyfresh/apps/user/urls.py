from django.conf.urls import url
from user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView,  AddressView, LogoutView # 导入视图类
from django.contrib.auth.decorators import login_required  # login_required登录验证装饰器

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    # url(r'^login$', views.login, name='login'),

    url(r'^register$', RegisterView.as_view(), name='register'),  # 用户注册
    url(r'^active/(.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    url(r'^login$', LoginView.as_view(), name='login'),  # 用户激活
    url(r'^logout$', LogoutView.as_view(), name='logout'),  # 用户激活
    url(r'^$', UserInfoView.as_view(), name='user'),  # 用户激活  使用登录验证
    url(r'^order$', UserOrderView.as_view(), name='order'),  # 用户激活
    url(r'^address$', AddressView.as_view(), name='address'),  # 用户激活

]
