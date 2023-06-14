from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, ModelAdmin
from .models import *
# Register your models here.


class Get_InAdmin(ModelAdmin):
    list_display = ('person_id','get_in_date', 'get_in_time',)
    list_filter = (
        ('get_in_date', DateFieldListFilter),
    )


class Get_OutAdmin(ModelAdmin):
    list_display = ('person_id', 'get_out_date', 'get_out_time',)
    list_filter = (
        ('get_out_date', DateFieldListFilter),
    )


admin.site.register(Person)
admin.site.register(Get_In, Get_InAdmin)
admin.site.register(Get_Out,Get_OutAdmin)
