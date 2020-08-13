from django.shortcuts import render,redirect,reverse
from user.models import User
from django.views import View

from django.http import HttpResponse
from django.conf import settings #导入设置文件
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #邮箱验证
from itsdangerous import SignatureExpired
from django.core.mail import BadHeaderError, send_mail
from celery_tasks.task import send_register_active_email #使用celery异步发送邮件
from django.contrib.auth import authenticate, login,  logout

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import re

from .models import Address #导入模型类
from user.models import User, Address
from goods.models import GoodsSKU
from django_redis import get_redis_connection

#初始化处理人
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

# def register(request):
#     '''注册'''
#     if request.method =='GET':
#         #显示注册也面
#         print('get')
#         return render(request, 'register.html')
#     else:
#         return register_handle(request)
#     # return render(request, 'register.html')
#
#
# def send(request, email, token):
#     '''发熊邮箱'''
#     emails = [email]  # 收件人list
#     try:
#         send_mail('确认你的邮箱', token, settings.EMAIL_FROM, emails)
#     except BadHeaderError:
#         return render(request, 'register.html', {'errmsg': '请输入正确邮箱'})
#     else:
#         return redirect(reverse('goods:index'))

def register_handle (request):
    '''进行注册处理'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    # 进行数据校验
    if not all([username, password, email]):
        # 数据不完整
        return render(request, 'register.html', {'errmsg':'数据不完整'})

    # # 校验邮箱
    # if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
    #     return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})
    # if allow != 'on':
    #     return render(request, 'register.html', {'errmsg':'请同意协议'})

    # 校验用户名是否重复
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 用户名不存在
        user = None
    else:
        # 用户名已存在
        return render(request, 'register.html', {'errmsg':'用户名已存在'})


    user = User.objects.create_user(username, email, password)
    user.is_active = 0
    user.save()
    # 进行业务处理: 进行用户注册

    # 加密用户的身份信息，生成激活token
    serializer = Serializer(settings.SECRET_KEY, 3600)#密匙，过期shij
    info = {'confirm': user.id} #加密的数据
    token = serializer.dumps(info)  # bytes，加密数据
    token ='http://127.0.0.1:8000/user/active/' +token.decode()  # 变成字符串
    # send(request, email, token)
    send_register_active_email(email, username, token)

    # 返回应答, 跳转到首页
    print('Yingda',reverse('goods:index'))
    return redirect(reverse('goods:index'))

# /user/register
class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        return register_handle(request)

#用户激活
class ActiveView(View):
    '''用户激活'''
    def get(self,request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        print(token)
        print(type(token))
        print('进行解密',token[34:])
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)#解密数据
            # 获取待激活用户的idss
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            print('zaijihuosss')
            # 跳转到登录页面
            print(reverse('user:login'))
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))

class LoginView(View):
    '''登录校验'''
    def get(self,request):
        '''
        显示登录页面
        '''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
            # 使用模板
            return render(request, 'login.html', {'username': username, 'checked': checked})
    # 接收数据
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print('LoginView,post  来了')
        # 校验数据
        if not all([username, password]):
            print('数据不完整')
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        print('user:',user)

        #记住登陆状态
        try:
            login(request, user)
        except AttributeError as a:
            print(a)
        # 跳转到首页
        print('reverse(goods:index)',reverse('goods:index'))
        response = redirect(reverse('goods:index'), {'name': username})  # HttpResponseRedirect

        # 判断是否需要记住用户名
        remember = request.POST.get('remember')
        if remember == 'on':
            # 记住用户名
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
        else:
            response.delete_cookie('username')
        return response
        # if user is  None:
        #     # 用户名密码正确
        #     if not user.is_active:
        #         # 用户已激活
        #         print('帐号已激活')
        #         # 记录用户的登录状态
        #         login(request, user)
        #
        #         # 跳转到首页
        #         response = redirect(reverse('goods:index'))  # HttpResponseRedirect
        #
        #         # 判断是否需要记住用户名
        #         remember = request.POST.get('remember')
        #
        #         if remember == 'on':
        #             # 记住用户名
        #             response.set_cookie('username', username, max_age=7 * 24 * 3600)
        #         else:
        #             response.delete_cookie('username')
        #
        #         # 返回response
        #         return response
        #     else:
        #         print('帐号为激活')
        #         # 用户未激活
        #         return render(request, 'login.html', {'errmsg': '账户未激活'})
        # else:
        #     print('用户密码错误')
        #     # 用户名或密码错误
        #     return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

class UserInfoView(LoginRequiredMixin,View):
    # Django会给request对象添加一个属性request.user
    # 如果用户未登录->user是AnonymousUser类的一个实例对象
    # 如果用户登录->user是User类的一个实例对象
    # request.user.is_authenticated()
    def get(self,request):
        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)
        # 获取用户的历史浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host='172.16.179.130', port='6379', db=9)
        con = get_redis_connection('default')

        history_key = 'history_%d' % user.id

        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)  # [2,3,1]

        # 从数据库中查询用户浏览的商品的具体信息
        goods_li = GoodsSKU.objects.filter(id__in=sku_ids)

        goods_res = []
        for a_id in sku_ids:
            for goods in goods_li:
                if a_id == goods.id:
                    goods_res.append(goods)

        # 遍历获取用户浏览的商品信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 组织上下文
        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li}

        # # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'user_center_info.html', context)

class UserOrderView(LoginRequiredMixin,View):

    def get(self, request):
        return render(request, 'user_center_order.html', {'user':'order'})


# /user/address
class AddressView(LoginRequiredMixin,View):
    '''用户中心-地址页'''

    def get(self, request):
        '''显示'''
        # 获取登录用户对应User对象
        user = request.user

        # 获取用户的默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True) # models.Manager
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None
        address = Address.objects.get_default_address(user)

        # 使用模板
        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        '''地址的添加'''

        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg':'手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address')) # get请求方式


