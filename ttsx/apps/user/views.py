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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import re
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

class ActiveView(View):
    '''用户激活'''
    def get(self,request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        print('进行解密')
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
        print('来了')
        # 校验数据
        if not all([username, password]):
            print('数据不完整')
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        print(user)
        print(username,password)
        if user is  None:
            # 用户名密码正确
            if not user.is_active:
                # 用户已激活
                print('帐号已激活')
                # 记录用户的登录状态
                login(request, user)

                # 跳转到首页
                response = redirect(reverse('goods:index'))  # HttpResponseRedirect

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                print('帐号为激活')
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            print('用户密码错误')
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))

class UserInfoView(LoginRequiredMixin,View):

    def get(self,request):
        return render(request,'user_center_info.html',{'page': 'user'})

class UserOrderView(LoginRequiredMixin,View):

    def get(self, request):
        return render(request, 'user_center_order.html', {'user':'order'})


# /user/address
class AddressView(LoginRequiredMixin,View):

    def get(self,request):
        return  render(request, 'user_center_site.html')
