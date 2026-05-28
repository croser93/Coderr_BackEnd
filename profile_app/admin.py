from django.contrib import admin
from profile_app.models import Profiles 

# Register your models here.
@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['type_id', 'user', 'location', 'type_display']

    def type_display(self, obj):
        return obj.user.profile.type
    type_display.short_description = 'Type'

    def type_id(self, obj):
        return obj.user.profile.id
    type_id.short_description = 'Id'