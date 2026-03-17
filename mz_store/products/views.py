from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, RangeFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Product,
    Review,
    ProductTag,
    FavoriteProduct,
    ProductImage,
    Cart,
    CartItem
)

from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    ProductTagSerializer,
    FavoriteProductSerializer,
    ProductImageSerializer,
    CartSerializer,
    CartItemSerializer
)

class ProductFilter(FilterSet):
    price_min = NumberFilter(field_name="price", lookup_expr='gte')
    price_max = NumberFilter(field_name="price", lookup_expr='lte')
    price_range = RangeFilter(field_name='price')

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max', 'price_range']

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [isAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    throttle_classes = [AnonRateThrottle]


class ReviewFilter(FilterSet):
    rating_range = RangeFilter(field_name="rating")

    class Meta:
        model = Review
        fields = ["product", "rating_range"]

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ["comment"]
    ordering_fields = ["rating"]
    throttle_classes = [UserRateThrottle]


class ProductTagViewSet(ModelViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'likes'


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    throttle_classes = [UserRateThrottle]

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    throttle_classes = [UserRateThrottle]