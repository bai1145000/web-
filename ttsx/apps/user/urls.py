from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from .views import UserInfoView,RegisterView,AddressView,ActiveView,UserOrderView,LoginView,LogoutView
app_name = 'user'

urlpatterns = ([
    # re_path(r'^register$', views.register, name='register'), # 注册
    # re_path(r'^register_handle$', views.register_handle, name='register_handle'), # 注册处理)

    re_path(r'register/$', RegisterView.as_view()),# 注册
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'), # 用户激活
    re_path(r'^login/', LoginView.as_view(), name='login'),  # 登录
    re_path(r'logout',LogoutView.as_view(), name='logout'),


    # re_path(r'^$', login_required(UserInfoView.as_view()), name='user'), # 用户中心-信息页
    # re_path(r'^order$', login_required(UserOrderView.as_view()), name='order'), # 用户中心-订单页
    # re_path(r'^address$', login_required(AddressView.as_view()), name='address'), # 用户中心-地址页

    re_path(r'^$', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    re_path(r'^order$', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    re_path(r'^address$', AddressView.as_view(), name='address'),  # 用户中心-地址页r


])
'''当一个请求到达的 re_path 被关联模式匹配时，这个类方法返回一个函数
。这个函数创建一个类的实例，调用 setup() 初始化它的属性，然后调用 dispatch() 方法。 
dispatch 观察请求并决定它是 GET 和 POST，等等。如果它被定义，那么依靠请求来匹配方法'''
