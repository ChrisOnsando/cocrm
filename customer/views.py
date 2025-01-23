from django.shortcuts import render
from .models import CustomerUserProfile
from django.shortcuts import render, redirect


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
