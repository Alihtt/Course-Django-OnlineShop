from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('register/verify/',views.UserRegisterVerifyCodeView.as_view(),name='verify_register_code'),
    
    path('login/',views.UserLoginView.as_view(),name='user_login'),
    path('login/verify/',views.UserLoginVerifyCodeView.as_view(),name='verify_login_code'),
    path('logout/',views.UserLogoutView.as_view(),name='user_logout')

]