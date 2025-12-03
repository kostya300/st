from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'status', 'created', 'initiator')
    list_filter = ('status', 'created', 'initiator')
    search_fields = ('first_name', 'last_name', 'email', 'address')
    readonly_fields = ('id','created',)
