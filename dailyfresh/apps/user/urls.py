from django.conf.urls import url
from user.views import RegisterView, ActiveView, LoginView  # 导入视图类

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    # url(r'^login$', views.login, name='login'),

    url(r'^register$', RegisterView.as_view(), name='register'),  # 用户注册
    url(r'^active/(.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    url(r'^login$', LoginView.as_view(), name='login'),  # 用户激活

]
