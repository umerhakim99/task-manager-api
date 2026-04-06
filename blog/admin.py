from django.contrib import admin
from .models import Contact




class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_at')
    search_fields = ('name', 'email')
    list_filter   = ('status',)
    list_editable = ('status',)



admin.site.register(Contact, ContactAdmin)
