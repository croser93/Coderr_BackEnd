
import django_filters

class OfferFilter(django_filters.FilterSet):
    """
    
    Custom PaginFilteration for GET /api/offers/ Endpoint.
    
    creator_id = return the element with the creator  Number
    min_price = return elements with > min_price
    min_delivery_time = return elements with > delivery_time
   
    
    """
    
    creator_id = django_filters.NumberFilter(field_name='user_id')
    min_price = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')