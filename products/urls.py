from django.urls import path
from .views import ProductListView, ProductDetailView, SearchResultsListView, RatingDetailView
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<uuid:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('<uuid:pk>/review/', RatingDetailView.as_view(), name='product_review'),
    path('<uuid:pk>/review/add_review/', views.add_review, name='review_and_rating'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('discount_management/', views.discount_management, name='discount_management'),
    path('<category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
]
