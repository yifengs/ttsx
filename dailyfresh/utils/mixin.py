from django.contrib.auth.decorators import login_required  # 导入登录认证包

class LoginRequiredMinxin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMinxin, cls).as_view(**initkwargs)
        return login_required(view)