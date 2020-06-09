from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from mainapp.forms import RegisterForm


# Create your views here.
@login_required
def index(request):
    return render(request, 'SearchByDistance.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout(request):
    logout(request)
# na mpei edo to main page 
@login_required
def business_page(request):
    return render(request, 'Business_Page.html')

@login_required
def change_info_cus(request):
    return render(request, 'Change_Info_Cus.html')

@login_required
def change_info_bus(request):
    return render(request, 'ChangeBusinessInfo.html')

@login_required
def customer(request):
    return render(request, 'CustomerPage.html')

@login_required
def business_submit(request):
    return render(request, 'NewBusinessSubmit.html')