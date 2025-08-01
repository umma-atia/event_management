from django.contrib import admin

# Register your models here.
from event.models import Category, Event, Participant

# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Participant)