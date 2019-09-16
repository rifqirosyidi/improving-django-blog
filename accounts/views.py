from django.contrib.auth import (
    login,
    logout,
    authenticate,
    get_user_model
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm


# Create your views here.
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    context = {
        'form': form,
        'title': "Login"
    }
    return render(request, "form.html", context)


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return redirect('/login')

    context = {
        "form": form,
        "title": "Register",
    }

    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')
