from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from.models import Category, Event
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.

def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        event.delete()
    return redirect('event_list')

def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')
        
        # Retrieve the Category object
        category = Category.objects.get(pk=category_id)
        # Create a new Event object
        event = Event(
            name=name, 
            category=category, 
            start_date=start_date, 
            end_date=end_date, 
            priority=priority, 
            description=description, 
            location=location, 
            organizer=organizer)

        # Redirect to the event list after creating the event
        return redirect('categorylist')
    else:
        categories = Category.objects.all()
        return render(request, 'event_management_system/create_event.html', {'categories': categories})

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.category_id = request.POST.get('category')
        event.start_date = request.POST.get('start_date')
        event.end_date = request.POST.get('end_date')
        event.priority = request.POST.get('priority')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.organizer = request.POST.get('organizer')
        event.save()
        return redirect('categoryt_list')
    else:
        return render(request, 'event_management_system/update_event.html', {'event': event})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'event_management_system/category_list.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')        
        # Create a new Category object
        Category.objects.create(name=name)
        return redirect('category_list')
    else:
        return render(request, 'event_management_system/create_category.html')
    
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if category.event_set.exists():
        messages.error(
            request,"Cannot delete category. It has associated events.")
    else:
        category.delete()
        messages.success(request,"Category deleted successfully.")
    return redirect('category_list')

def category_events(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    events = category.event_set.all()
    return render(request, 'event_management_system/category_events.html', {'category': category, 'events': events})

def event_chart(request):
    categories = Category.objects.all()
    pending_counts = {}
    for category in categories:
        pending_counts[category.name] = Event.objects.filter(
            category=category, 
            start_date__gte=timezone.now()
        ).count()
    return render(request, 'event_management_system/event_chart.html', {'pending_counts': pending_counts})
        