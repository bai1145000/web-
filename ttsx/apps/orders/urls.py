from django.urls import path,re_path
from orders.views import OrderPlaceView, OrderCommitView,OrderPayView,CommentView

app_name ='orders'

urlpatterns = [
    re_path(r'^place$', OrderPlaceView.as_view(), name='place'), # 提交订单页面显示
    re_path(r'^commit$', OrderCommitView.as_view(), name='commit'), # 订单创建
    re_path(r'^pay$', OrderPayView.as_view(), name='pay'),  # 订单支付
    re_path(r'^comment/(?P<order_id>.+)$', CommentView.as_view(), name='comment'),  # 订单评论
]
