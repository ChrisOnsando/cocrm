from django.shortcuts import render
from .models import (
    CustomerUserProfile,
    Customer_details,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages

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

def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)

    if request.method == "POST":
        customer.name = request.POST.get('name')
        customer.city = request.POST.get('city')
        customer.state = request.POST.get('state')
        customer.country = request.POST.get('country')
        customer.phone = request.POST.get('phone')
        customer.save()

        messages.success(request, "Customer updated successfully!")
        return redirect('customer_dashboard')  

    return render(request, 'edit_customer.html', {'customer': customer})
