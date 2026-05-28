import django_filters
from reviews_app.models import ReviewModel

class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(field_name='business_user_id')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer_id')

    class Meta:
        model = ReviewModel
        fields = ['business_user_id', 'reviewer_id']
