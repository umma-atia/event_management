from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from event.forms import EventCreateForm, CategoryForm, ParticipantForm
from event.models import Event, Category, Participant
from django.contrib.auth.models import User
from django.db.models import Prefetch
from datetime import date
import datetime
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.views import View
from django.views.generic import UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_manager(user):
    return user.groups.filter(name='Organizer').exists()

def is_Participant(user):
    return user.groups.filter(name='User').exists()

def is_manager_or_admin(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()

@login_required
@user_passes_test(is_manager_or_admin, login_url='no-permission')
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


@login_required
@permission_required("event.view_event", login_url='no-permission')
def event_list(request):
    events = Event.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "dashboard/event_list.html", {"events": events})


class EventList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = "dashboard/event_list.html"
    context_object_name = "events"
    permission_required = "event.view_event"
    login_url = 'no-permission'

    def get_queryset(self):
        events = Event.objects.select_related("category").prefetch_related("participants").all()
        return events


@login_required
@permission_required("event.add_event", login_url='no-permission')
def create_event(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('create-event')
    else:
        form = EventCreateForm()  # for GET

    context = {'form': form}
    return render(request, 'event_form.html', context)


class CreateEvent(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'event.add_event'
    login_url = 'sign-in'
    template_name = 'event_form.html'

    def get(self, request, *args, **kwargs):
        form = EventCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('create-event')
        return render(request, self.template_name, {'form': form})


@login_required
@permission_required("event.change_event", login_url='no-permission')
def update_event(request,id):
    event = Event.objects.get(id=id)
    form = EventCreateForm(instance = event) #for GET 

    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event-update',id)
    context = {'form':form}
    return render(request, 'event_form.html', context)


class UpdateEvent(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'event_form.html'
    context_object_name = 'event'
    permission_required = 'event.change_event'
    login_url = 'no-permission'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Event Updated Successfully")
            return redirect('event-update', self.object.id)

        return redirect('event-update', self.object.id)        
    
    

@login_required
@permission_required("event.delete_event", login_url='no-permission')
def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()

        messages.success(request, "Event deleted Successfully")
        return redirect('event-list') # url name disi
    else:
        messages.success(request, "Something went wrong")
        return redirect('event-list')   


class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('event-list')
    permission_required = 'event.delete_event'
    login_url = 'no-permission'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Event deleted Successfully")
        return redirect(self.success_url)


    def handle_no_permission(self):
        messages.error(self.request, "Something went wrong")
        return redirect('event-list')


@login_required
@permission_required("event.view_event", login_url='no-permission')
def event_detail(request,id):
    event = Event.objects.prefetch_related('participants').get(id=id)
    participants = event.participants.all()
    context={
        'event': event,
        'participants': participants}
    return render(request, 'dashboard/detail.html',context)


class EventDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = 'dashboard/detail.html'
    context_object_name = 'event'
    permission_required = 'event.view_event'
    login_url = 'no-permission'

    def get_object(self):
        queryset = Event.objects.prefetch_related('participants')
        event = queryset.get(id=self.kwargs['id'])
        return event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = self.object.participants.all()
        return context


@login_required
def buy_ticket(request,id):
    if request.method == 'POST':
        event=Event.objects.get(id=id)
        Participant.objects.create(event=event, user=request.user)
        return redirect('dashboard')   


@login_required
@permission_required("event.add_participant", login_url='no-permission')
def create_participant(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('participant-list')  # url name disi
    return render(request, "dashboard/participant_form.html", {"form": form, "title": "Create Participant"})



@login_required
@permission_required("event.view_event", login_url='no-permission')
def participant_list(request):
    participants = User.objects.filter(groups__name='User').order_by('username')

    return render(request, 'dashboard/participant_list.html', {'participants': participants})


@login_required
@permission_required("event.change_participant", login_url='no-permission')
def update_participant(request, id):
    participant = Participant.objects.get(id=id)
    form = ParticipantForm(instance=participant)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant-list')
    return render(request, "dashboard/participant_form.html", {"form": form, "title": "Edit Participant"})



@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_participant(request, id):
    if request.method == 'POST':
        participant = User.objects.get(id=id)
        participant.delete()

        messages.success(request, "Participant deleted Successfully")
        return redirect('participant-list') # url name disi
    else:
        messages.success(request, "Something went wrong")
        return redirect('manager_dashboard')


@login_required
@permission_required("event.view_category", login_url='no-permission')
def category_list(request):
    categories = Category.objects.all()
    return render(request, "dashboard/category_list.html", {"categories": categories})


@login_required
@permission_required("event.add_category", login_url='no-permission')
def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')  # url name disi
    return render(request, "dashboard/category_form.html", {'form': form, "title": "Create Category"})   


@login_required
@permission_required("event.change_category", login_url='no-permission')
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


@login_required
@permission_required("event.delete_category", login_url='no-permission')    
def delete_category(request, id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()

        messages.success(request, "Category deleted Successfully")
        return redirect('category-list') # url name disi
    else:
        messages.success(request, "Something went wrong")
        return redirect('manager_dashboard')



@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_Participant(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')    


