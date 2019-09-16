from django.contrib.auth import (
    login,
    logout,
    authenticate,
    get_user_model
)
from django.shortcuts import render
from .forms import UserLoginForm


# Create your views here.
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

    context = {
        'form': form,
        'title': "Login"
    }
    return render(request, "form.html", context)


def register_view(request):
    return render(request, "form.html", {})


def logout_view(request):
    return render(request, "form.html", {})
