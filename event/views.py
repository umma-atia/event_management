from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from event.forms import EventCreateForm, CategoryForm, ParticipantForm
from event.models import Event, Category, Participant
from datetime import date
import datetime
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages

def manager_dashboard(request):
    type = request.GET.get('type','all')
    print(type)

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming_events=Count('id', filter=Q(date__gt=date.today()) | Q(date=date.today())),
        past_events=Count('id', filter=Q(date__lt=date.today()))
    )
    
    total_unique_participants = Participant.objects.values('id').distinct().count()
    today_events = Event.objects.filter(date=date.today()).select_related('category')

    if type=='upcoming':
        events = base_query.filter(Q(date__gt=date.today()) | Q(date=date.today()))
    elif type=='past_events':
        events = base_query.filter(date__lt=date.today())
    elif type=='all_participants':
        events = Event.objects.prefetch_related('participants')
    if type=='all':
        events = base_query.all()    

    context = {
        'counts':counts,
        'all_events': events,
        'today_events': today_events,
        'total_unique_participants': total_unique_participants,
    }       
    return render(request, 'dashboard/manager_dashboard.html', context)


def event_list(request):
    events = Event.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "dashboard/event_list.html", {"events": events})


def create_event(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('create-event')
    else:
        form = EventCreateForm()  # for GET

    context = {'form': form}
    return render(request, 'event_form.html', context)


def update_event(request,id):
    event = Event.objects.get(id=id)
    form = EventCreateForm(instance = event) #for GET 

    if request.method == 'POST':
        form = EventCreateForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event-update',id)
    context = {'form':form}
    return render(request, 'event_form.html', context)
    

def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()

        messages.success(request, "Event deleted Successfully")
        return redirect('event-delete') # url name disi
    else:
        messages.success(request, "Something went wrong")
        return redirect('event-delete')   


def event_detail(request,id):
    event = Event.objects.prefetch_related('participants').get(id=id)
    participants = event.participants.all()
    context={
        'event': event,
        'participants': participants}
    return render(request, 'dashboard/detail.html',context)


@login_required
def buy_ticket(request,id):
    if request.method == 'POST':
        event=Event.objects.get(id=id)
        Participant.objects.create(event=event, user=request.user)
        return redirect('dashboard')   


def create_participant(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('participant-list')  # url name disi
    return render(request, "dashboard/participant_form.html", {"form": form, "title": "Create Participant"})


def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, "dashboard/participant_list.html", {"participants": participants})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "dashboard/category_list.html", {"categories": categories})


def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')  # url name disi
    return render(request, "dashboard/category_form.html", {'form': form, "title": "Create Category"})   


def update_category(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)  #for GET
    
    if request.method == 'POST':
        form = CategoryForm(request.POST or None, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")            
            return redirect('category-list')  # url name disi
    return render(request, "dashboard/category_form.html", {"form": form, "title": "Edit Category"})

    
def delete_category(request, id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()

        messages.success(request, "Category deleted Successfully")
        return redirect('category-list') # url name disi
    else:
        messages.success(request, "Something went wrong")
        return redirect('manager_dashboard')



def update_participant(request, id):
    participant = Participant.objects.get(id=id)
    form = ParticipantForm(instance=participant)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant-list')
    return render(request, "events/participant_form.html", {"form": form, "title": "Edit Participant"})


def delete_participant(request, id):
    if request.method == 'POST':
        participant = Participant.objects.get(id=id)
        participant.delete()

        messages.success(request, "Participant deleted Successfully")
        return redirect('category-list') # url name disi
    else:
        messages.success(request, "Something went wrong")
        return redirect('manager_dashboard')