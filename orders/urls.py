from django.urls import path
from .views import OrdersPageView, OrderListView, OrderDetailView, MyOrderListView
from . import views

urlpatterns = [
    path('', OrdersPageView.as_view(), name='orders'),
    path('create/', views.order_create, name='order_create'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('detail_order/<pk>/', OrderDetailView.as_view(), name='detail_order'),
    # path('my_orders/', views.my_orders, name='my_orders'),
    path('my_orders/', MyOrderListView.as_view(), name='my_orders'),
]