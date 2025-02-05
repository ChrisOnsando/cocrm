from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import UserProfile

def home(request):
    user_ = None
    user_id = request.session.get('user_id')

    if user_id:
        user_ = UserProfile.objects.filter(id=user_id).first()  

    return render(request, 'home.html', {'user_': user_})

def logoutUser(request):
    logout(request)
    return redirect('home')  

def render_page(request, template_name):
    return render(request, f'{template_name}.html')

def register(request):
    return render_page(request, 'register')

def about_us(request):
    return render_page(request, 'AboutUs')

def contact_us(request):
    return render_page(request, 'ContactUs')

def services(request):
    return render_page(request, 'services')

def terms(request):
    return render_page(request, 'terms')

def analytics(request):
    return render_page(request, 'analytics')
