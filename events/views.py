from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from events.models import Event, Category
from django.contrib.auth.models import User
from events.forms import EventForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


@login_required
def dashboard(request):
    today = date.today()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    context = {
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
    }

    return render(request, "dashboard.html", context)

@login_required
@permission_required('events.view_event', login_url='no_permission')
def event_list(request):
    events = Event.objects.prefetch_related("participants").all()
    return render(request, "event_list.html", {"events": events})

@login_required
@permission_required('events.add_event', login_url='no_permission')
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event create successfully")
            return redirect('view_event')
          
    return render(request, 'event_form.html', {'form': form})

@login_required
@permission_required('events.change_event', login_url='no_permission')
def event_update(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(instance = event)
    if(request.method == 'POST'):
        form = EventForm(request.POST, instance = event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_update', id)
    return render(request, "event_form.html", {"form":form})

@login_required
@permission_required('events.delete_event', login_url='no_permission')
def event_delete(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    else:
        messages.error(request, "Something error!")
        return redirect('event_list')
    

@login_required
@permission_required('events.view_event', login_url='no_permission')
def view_event(request):
    type = request.GET.get('type', 'all') 
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    today = date.today() 

    if type == 'upcoming':
        events = base_query.filter(date__gte=today)
    elif type == 'past':
        events = base_query.filter(date__lt=today) 
    elif type == 'all':
        events = base_query.all()
    else:
        events = []

    participants_count = User.objects.count() 
    
    context = {
        "events": events,
        "participants_count": participants_count,
    }

    return render(request, "view_event.html", context)

@login_required
@permission_required('events.view_event', login_url='no_permission')
def view_detail(request, id):
    event = Event.objects.select_related("category").prefetch_related("participants").get(id=id)
    return render(request, 'event_detail.html', {"event":event})
