from django.urls import path
from event.views import manager_dashboard, create_event, update_event, delete_event, event_detail, buy_ticket

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name = 'manager_dashboard'),
    path('create-event/', create_event, name="create-event"),
    path('update-event/<int:id>/', update_event, name='update'),
    path('delete-event/<int:id>/', delete_event, name='delete'),
    path('event-detail/<int:id>/', event_detail, name= 'detail'),
    path('buy-ticket/<int:id>/', buy_ticket, name='buy_ticket')
     
]
