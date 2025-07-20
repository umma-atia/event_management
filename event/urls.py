from django.urls import path
from event.views import manager_dashboard, create_event, update_event, delete_event, event_detail, buy_ticket, category_list, create_category, participant_list, create_participant, event_list, update_category, delete_category, update_participant, delete_participant

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name = 'manager_dashboard'),
    path('create-event/', create_event, name="create-event"),
    path('update-event/<int:id>/', update_event, name='event-update'),
    path('delete-event/<int:id>/', delete_event, name='event-delete'),
    path('event-detail/<int:id>/', event_detail, name= 'detail'),
    path('buy-ticket/<int:id>/', buy_ticket, name ='buy_ticket'),
    path('event/', event_list, name='event-list'),
    path('categories/', category_list, name='category-list'),
    path('categories/create/', create_category, name='category-create'),
    path('categories/<int:id>/edit/', update_category, name='category-update'),
    path('categories/<int:id>/delete/', delete_category, name='category-delete'),
    path('participants/', participant_list, name='participant-list'),
    path('participants/create/', create_participant, name ='participant-create'),
    path('participants/<int:id>/edit/', update_participant, name ='participant-update'),
    path('participants/<int:id>/delete/', delete_participant, name ='participant-delete')
     
]
