from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from account.forms import UserForm

# Create your views here.
def index(request):
    return render(request, 'account/index.html')

def user_register(request):
    registered = False
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    elif request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('account:user_login'))
    else:
        user_form = UserForm()
    return render(request, 'registration/user_register.html', {'registered': registered, 'user_form': user_form})

def user_login(request):
    if request.method == "POST":
        username = request.POST('email')
        password = request.POST('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('account::index'))
            else:
                message.error(request, 'Account not active. Kindly contact ADMIN')
        else:
            message.error(request, "Your email and password didn't matched. Please try again")
            return HttpResponseRedirect(reverse('account:user_login'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:imdex'))
        else:
            return render(request, 'registration/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:index'))
