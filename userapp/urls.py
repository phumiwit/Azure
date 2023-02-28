from django.urls import path
from userapp import views
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.urls import path, re_path
urlpatterns = [
    path('userdetail',views.userdetail),
    path('userdetail/', views.userdetail, name='userdetail'),
    path("usersignup",views.usersignup),
    path("",views.userlogin,name='userlogin'),
    path("userlogout",views.userlogout),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_invalid/', views.password_reset_invalid, name='password_reset_invalid'),
    path('confirm_delete_user/<int:user_id>/', views.confirm_delete_user, name='confirm_delete_user'),
]