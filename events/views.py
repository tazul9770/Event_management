from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from events.models import Event, Participant, Category
from events.forms import EventForm

def home(request):
    return render(request, 'base.html')

def dashboard(request):
    today = date.today()

    # Querying required data
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    context = {
        "total_events": total_events,
        "total_participants": total_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
    }

    return render(request, "dashboard.html", context)

def event_list(request):
    events = Event.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "event_list.html", {"events": events})

def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event create successfully")
            return redirect('create_event')
          
    return render(request, 'event_form.html', {'form': form})

def event_detail(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    return render(request, 'event_detail.html', {'events': events})

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

def event_delete(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    else:
        messages.error(request, "Something error!")
        return redirect('event_list')
    

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

    participants_count = Participant.objects.count() 
    
    context = {
        "events": events,
        "participants_count": participants_count,
    }

    return render(request, "view_event.html", context)

    
    
        

