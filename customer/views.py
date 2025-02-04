from django.shortcuts import render
from .models import (
    CustomerUserProfile,
    Customer_details,
    CustomerInteraction,
    task,
    SupportTicket,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from .forms import SupportTicketForm


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

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)

    if request.method == 'POST':
        customer.delete()  
        return redirect('customer_dashboard')

    return render(request, 'delete_customer.html', {'customer': customer})


def task_list(request, customer_id):
    tasks = task.objects.filter(customer_id=customer_id)
    return render(request, 'task_list.html', {'tasks': tasks, 'customer_id': customer_id})

def add_task(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)  
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        completed = request.POST.get('completed') == 'on'

        new_task = task.objects.create(  
            customer=customer,
            title=title,
            description=description,
            due_date=due_date,
            completed=completed
        )
        messages.success(request, 'Task created successfully!')
        return redirect('task_list', customer_id=customer.id)

    return render(request, 'add_task.html', {'customer_id': customer.id, 'customer': customer})

def edit_task(request, customer_id, task_id):
    task_instance = get_object_or_404(task, id=task_id, customer_id=customer_id)

    if request.method == 'POST':
        task_instance.title = request.POST.get('title')
        task_instance.description = request.POST.get('description')
        task_instance.due_date = request.POST.get('due_date')
        task_instance.completed = request.POST.get('completed') == 'on'

        task_instance.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list', customer_id=customer_id)

    return render(request, 'edit_task.html', {'task': task_instance, 'customer_id': customer_id})


def delete_task(request, customer_id, task_id):
    task_instance = get_object_or_404(task, id=task_id, customer_id=customer_id)
    task_instance.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list', customer_id=customer_id)

def task_list(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)
    tasks = task.objects.filter(customer=customer)  
    return render(request, 'task_list.html', {'tasks': tasks, 'customer_id': customer.id})

def task_detail(request, customer_id, task_id):
    task_instance = get_object_or_404(task, id=task_id, customer_id=customer_id)
    return render(request, 'task_detail.html', {'task': task_instance, 'customer_id': customer_id})
def ticket_list(request):

    tickets = SupportTicket.objects.all()

    return render(request, 'ticket_list.html', {'tickets': tickets})
def ticket_detail(request, ticket_id):
    """View to display details of a specific ticket."""
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})

def create_ticket(request):
    """View to create a new support ticket."""
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            try:
                customer_profile = CustomerUserProfile.objects.get(username=request.user.username)  # Or username=request.user.username
                ticket.customer = customer_profile
                ticket.save()
                messages.success(request, "Ticket created successfully.")
                return redirect('ticket_list')
            except CustomerUserProfile.DoesNotExist:
                return redirect('ticket_list') 
    else:
        form = SupportTicketForm()

    return render(request, 'create_ticket.html', {'form': form})


def customer_interaction_list(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)
    interactions = customer.interactions.all()
    return render(
        request,
        'customer_interaction_list.html',
        {
            'customer': customer,
            'interactions': interactions
        }
    )

def create_customer_interaction(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)
    if request.method == 'POST':
        interaction_type = request.POST.get('interaction_type')
        notes = request.POST.get('notes')
        CustomerInteraction.objects.create(
            customer=customer,
            interaction_type=interaction_type,
            notes=notes
        )
        messages.success(request, 'Interaction added successfully!')
        return redirect('customer_interaction_list', customer_id=customer.id)
    return render(request, 'create_customer_interaction.html', {'customer': customer})

def customer_edit_interaction(request, customer_id, interaction_id):
    interaction = get_object_or_404(CustomerInteraction, id=interaction_id, customer_id=customer_id)
    if request.method == 'POST':
        interaction.interaction_type = request.POST.get('interaction_type')
        interaction.notes = request.POST.get('notes')
        interaction.save()
        messages.success(request, 'Interaction updated successfully!')
        return redirect('select_customer_for_interaction')
    return render(request, 'customer_edit_interaction.html', {'interaction': interaction})

def customer_delete_interaction(request, customer_id, interaction_id):
    interaction = get_object_or_404(CustomerInteraction, id=interaction_id, customer_id=customer_id)
    if request.method == 'POST':
        interaction.delete()
        messages.success(request, 'Interaction deleted successfully!')
        return redirect('select_customer_for_interaction')
    return render(request, 'customer_delete_interaction.html', {'interaction': interaction})


def select_customer_for_interaction(request):
    customers = Customer_details.objects.all()
    return render(request, 'select_customer_for_interaction.html', {'customers': customers})

def view_customer_interaction(request, customer_id):
    customer = get_object_or_404(Customer_details, id=customer_id)
    interactions = CustomerInteraction.objects.filter(customer=customer)
    return render(request, 'view_customer_interaction.html', {
        'customer': customer,
        'interactions': interactions
    })
