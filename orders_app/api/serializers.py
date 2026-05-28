from rest_framework import serializers
from orders_app.models import OrdersModel
from offers_app.models import DetailModel

class OrdersSerializer(serializers.ModelSerializer):
    """
    Serializer for add a Order from Offer.

    calculated fields:
    - offer_detail_id : return the Offer id with content.
    - create : Create a Order based on the Offer id
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrdersModel
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 
                    'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at', 'offer_detail_id']
        read_only_fields = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                            'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    def create(self, validated_data):
        detail = DetailModel.objects.get(pk=validated_data['offer_detail_id'])
        order = OrdersModel.objects.create(
            customer_user=validated_data['customer_user'],
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress',
        )
        return order
