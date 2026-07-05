from django.urls import path

from masters import views
app_name = 'masters'

urlpatterns = [
    path('hello',views.hello,name='hello'),
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('vendor_temp',views.vendor_temp,name='vendor_temp'),
    path('create_vendor',views.create_vendor,name='create_vendor'),
    path('vendor_list',views.vendor_list,name='vendor_list'),

    path('gl_temp', views.gl_temp, name='gl_temp'),
    path('create_gl', views.create_gl, name='create_gl'),
    path('gl_list', views.gl_list, name='gl_list'),

    path('branch_temp', views.branch_temp, name='branch_temp'),
    path('create_branch', views.create_branch, name='create_branch'),
    path('branch_list', views.branch_list, name='branch_list'),

]
