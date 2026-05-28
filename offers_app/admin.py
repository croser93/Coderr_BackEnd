from django.contrib import admin
from .models import Offers, OffersDetail

@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'offer_detail_basic', 'offer_detail_standart', 'offer_detail_premium' ]

    def offer_detail_basic(self, obj):
        detail = obj.details.filter(offer_type='basic').first()
        return detail.title if detail else '-'
    offer_detail_basic.short_description = 'Basic'

    def offer_detail_standart(self, obj):
        detail = obj.details.filter(offer_type='standard').first()
        return detail.title if detail else '-'
    offer_detail_standart.short_description = 'Standard'

    def offer_detail_premium(self, obj):
        detail = obj.details.filter(offer_type='premium').first()
        return detail.title if detail else '-'
    offer_detail_premium.short_description = 'Premium'

@admin.register(OffersDetail)
class OffersDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'offer_type', 'offer_id', 'offer_title']

    def offer_id(self, obj):
            return obj.offer.id
    offer_id.short_description = 'offer_id'

    def offer_title(self, obj):
            return obj.offer.title
    offer_title.short_description = 'offer_title'