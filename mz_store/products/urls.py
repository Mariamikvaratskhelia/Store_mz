from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# Base routers
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('favorite-products', views.FavoriteProductViewSet)
router.register('tags', views.ProductTagViewSet)
router.register('carts', views.CartViewSet)
router.register("reviews", views.ReviewViewSet)

# Nested router for product images
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('images', views.ProductImageViewSet, basename='product-images')

# Combine router URLs
urlpatterns = []
urlpatterns += router.urls
urlpatterns += product_router.urls