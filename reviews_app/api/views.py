from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .permissions import UserOrAdmin, IsCustomerUserOrAdmin
from .serializer import ReviewSerializer
from .filters import ReviewFilter
from reviews_app.models import ReviewModel


class ReviewListView(APIView):
    """
     View for Reviews

    Endpoints:
    - POST /api/reviews/ - POST a review where user is Business User.
    - GET /api/reviews/ - Get a list of all Reviews.
    """

    permission_classes = [IsAuthenticated, IsCustomerUserOrAdmin]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = ReviewSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(reviewer=self.request.user)
                return Response(serializer.data, status=201)
            else:
                return Response({"error": "Fehlerhafte Anfrage. Der Benutzer hat möglicherweise bereits eine Bewertung für das gleiche Geschäftsprofil abgegeben."}, status=400)
        except ReviewModel.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)

    def get(self, request):
        reviews = ReviewFilter(request.query_params,
                               queryset=ReviewModel.objects.all()).qs
        ordering = request.query_params.get('ordering')
        if ordering in ['rating', 'updated_at', '-rating', '-updated_at']:
            reviews = reviews.order_by(ordering)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)


class ReviewDetailView(APIView):
    """
    Single View for Review.

    Endpoints:
    - PATCH /api/reviews/{id}/ - Update a signle review.
    - DELETE /api/reviews/{id}/ - Delete a single review.
    """

    permission_classes = [IsAuthenticated, UserOrAdmin]

    def patch(self, request, pk):
        try:
            review = ReviewModel.objects.get(pk=pk)
            self.check_object_permissions(request, review)
            serializer = ReviewSerializer(
                review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({"error": "Bad Request. Der Anfrage-Body enthält ungültige Daten.."}, status=400)

        except ReviewModel.DoesNotExist:
            return Response({"error": "Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden."}, status=404)

    def delete(self, request, pk):
        try:
            review = ReviewModel.objects.get(pk=pk)
            self.check_object_permissions(request, review)
            review.delete()
            return Response(status=204)
        except ReviewModel.DoesNotExist:
            return Response({"error": "Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden."}, status=404)
