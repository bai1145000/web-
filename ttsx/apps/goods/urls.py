from django.urls import path,re_path
from . import views
app_name = 'goods'
urlpatterns = [
    re_path(r'^index/', views.index, name='index'),
]

