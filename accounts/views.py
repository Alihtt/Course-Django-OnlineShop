from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm,UserVerifyCodeForm,UserLoginForm
from .models import OtpCode,User
from utilts import send_otp_code
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
import datetime
import random
from django.contrib.auth.mixins import LoginRequiredMixin

class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
        
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = random.randint(1000,9999)
            send_otp_code(cd['phone'],code)
            OtpCode.objects.create(phone_number=cd['phone'],code=code)
            
            request.session['user_registeration_info'] = {
                'phone_number':cd['phone'],
                'email':cd['email'],
                'full_name':cd['full_name'],
                'password':cd['password']
            }
            
            messages.success(request,'We sent you a code','success')
            return redirect('accounts:verify_register_code')
        return render(request,self.template_name,{'form':form})
    
class UserRegisterVerifyCodeView(View):
    form_class = UserVerifyCodeForm
    
    def get(self,request):
        form = self.form_class()
        return render(request,'accounts/verify.html',{'form':form})
    
    def post(self,request):
        user_session = request.session['user_registeration_info']
        form = self.form_class(request.POST)
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                then = code_instance.created
                now = timezone.now()
                duration = now - then
                duration_in_s = duration.total_seconds()
                if duration_in_s < 120:
                    User.objects.create_user(user_session['phone_number'],user_session['email'],user_session['full_name'],user_session['password'])
                    code_instance.delete()
                    messages.success(request,'Successfully verified!','success')
                    return redirect('home:home')
                else:
                    code_instance.delete()
                    messages.error(request,'Your code expired','danger')
                    return redirect('accounts:user_register')
            else:
                messages.error(request,'Your code is wrong !!!','danger')
                return redirect('accounts:verify_register_code')
        return redirect('home:home')
    
    
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
        
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone_number=cd['phone'],password=cd['password'])
            if user is not None:
                code = random.randint(1000,9999)
                send_otp_code(cd['phone'],code)
                OtpCode.objects.create(phone_number=cd['phone'],code=code)
                request.session['user_login_info'] = {
                    'phone_number':cd['phone'],
                    'password':cd['password'],
                }
                messages.success(request,'We sent you a code','success')
                return redirect('accounts:verify_login_code')
            else:
                messages.error(request,'Your phone number/password is wrong!','danger')
                
        return render(request,self.template_name,{'form':form})
        
class UserLoginVerifyCodeView(View):
    form_class = UserVerifyCodeForm
    
    def get(self,request):
        form = self.form_class()
        return render(request,'accounts/verify.html',{'form':form})
    
    def post(self,request):
        user_session = request.session['user_login_info']
        form = self.form_class(request.POST)
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                then = code_instance.created
                now = timezone.now()
                duration = now - then
                duration_in_s = duration.total_seconds()
                if duration_in_s < 120:
                    user = User.objects.get(phone_number=user_session['phone_number'])
                    login(request,user)
                    code_instance.delete()
                    messages.success(request,'You logged in successfully!','success')
                    return redirect('home:home')
                else:
                    code_instance.delete()
                    messages.error(request,'Your code expired','danger')
                    return redirect('accounts:user_login')
            else:
                messages.error(request,'Your code is wrong !!!','danger')
                return redirect('accounts:verify_login_code')
        return redirect('home:home')
    

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'You logged out successfully','success')
        return redirect('home:home')
    
    
    
    
    
    
    
    