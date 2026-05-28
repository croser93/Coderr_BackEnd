from django.contrib import admin
from .models import Reviews
# Register your models here.

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'reviewer', 'business_user', 'rating']

    def reviewer(self, obj):
        return obj.reviewer.username
    reviewer.short_description = 'Reviewer'

    def business_user(self, obj):
        return obj.business_user.username
    business_user.short_description = 'Business User'
