from django.contrib import admin
from home.models import Setting, ContactMessages
# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','company','update_at','status']

class ContactMessagesAdmin(admin.ModelAdmin):
    list_display = ['name','subject','update_at','status','note']
    readonly_fields = ('name','email','subject','telephone','message','ip_address')
    list_filter = ['status']

admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessages,ContactMessagesAdmin)