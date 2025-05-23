import time
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.contrib.auth import logout
from django.core.cache import cache
from django.urls import reverse
from users.forms import MyAuthForm, MyRegForm
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


def log_in(request):
    if request.method == 'POST':
        form = MyAuthForm(data=request.POST)
        if form.is_valid(): 
            user = form.get_user() 
            login(request, user)
            return redirect('users:users_lst')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
    

def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('users:log_in') )
    

def my_registration(request):
    
    if request.user.is_authenticated:
            print("Вы уже авторизированны.")
            return HttpResponseRedirect(reverse('users:users_lst') )
    form = MyRegForm(request.POST) 
    if request.method == 'POST':
        if form.is_valid():
            reg_form_passw_value1 = form.cleaned_data.get('password1')
            reg_form_passw_value2 = form.cleaned_data.get('password2')
            reg_form_email_value = form.cleaned_data.get('email')
            if reg_form_email_value in [i.email for i in CustomUser.objects.all()]:
                print('Account already exists')
                messages.error(request, 'Account already exists')
                
                return HttpResponseRedirect(reverse('users:log_in') )
            if not reg_form_passw_value1 == reg_form_passw_value2:#Пока не убрал, валидация паролей и в форме есть, и здесь.
                # Если только здесь, то тест не проходил 
                messages.warning(request, 'Passwords not equal')
                context = { 
                    'form':form
                            } 
                return render(request, 'registration/register.html', context) 
            customuser = CustomUser.objects.create( email=reg_form_email_value)
            customuser.set_password(reg_form_passw_value1)
            customuser.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('users:users_lst') )
 
    else: 
        form = MyRegForm() 
    context = { 
        'form':form
    } 
    return render(request, 'registration/register.html', context)

def users_lst(request):
       
        customuser_queryset = CustomUser.objects.all()
        context = {
                            'customuser_queryset':customuser_queryset,
                        }
        return render(request, 'users/templates/users_lst.html', context)


