from django.contrib import admin
from .models import elevator,Person
# Register your models here.

@admin.register(elevator)
class ElevatorAdmin(admin.ModelAdmin):
    list_display=['id','elevator_id','current_floor','operational','direction','is_busy','door']
    
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display=['id','requesting_floor','destination_floor','elevator']
