from django.shortcuts import render
from .models import (
    CustomerUserProfile,
    Customer_details,
)
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        password_confirmation = request.POST.get('password_confirmation')

        if password == password_confirmation:
            try:
                user = CustomerUserProfile(username=username, password=password, email=email)
                if user:
                    return redirect('customer_login')  
            except Exception as e:
                return render(request, 'customer_signup.html', {'error': 'Error creating account.'})
        else:
            return render(request, 'customer_signup.html', {'error': 'Passwords do not match.'})

    return render(request, 'customer_signup.html')



def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = CustomerUserProfile(username=username, password=password)
        if user:
            return redirect('customer_dashboard')  
        else:
            return render(request, 'customer_login.html', {'error': 'Invalid credentials.'})
    return render(request, 'customer_login.html')

def customer_dashboard(request):

    customer_details = Customer_details.objects.all()  

    context = {
        'details': customer_details,
    }
    return render(request, 'customer_dashboard.html', context)
def logout_view(request):
    logout(request)
    return redirect('home')


def create_customer(request):
    if request.method == "POST":
        name = request.POST.get('name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        newCustomer  = Customer_details(
            name=name,
            city=city,
            state=state,
            country=country,
            phone=phone
        )
        newCustomer.save()
        return redirect('customer_dashboard')
    return render(request, 'create_customer.html')
