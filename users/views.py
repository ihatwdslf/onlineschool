from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


# сторінка реєстрації
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            form.save_m2m()
            # одразу логінимо після реєстрації
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


# сторінка входу
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# вихід з акаунту
def logout_view(request):
    logout(request)
    return redirect('/login/')