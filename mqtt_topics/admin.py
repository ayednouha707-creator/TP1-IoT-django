from django.contrib import admin
from .models import Mesure


@admin.register(Mesure)
class MesureAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'value', 'date_prise', 'date_reception')
    list_filter = ('topic',)
    ordering = ('-date_prise',)