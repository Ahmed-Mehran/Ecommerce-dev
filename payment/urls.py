from django.urls import path

from . import views

urlpatterns = [

    path('checkout', views.checkout, name='checkout'),

    path('order-confirmation', views.order_confirmation, name='order-confirmation'),

    path('save_order', views.save_order, name='save_order'),
    
    path('payment-success', views.payment_success, name='payment-success'),

    path('payment-failed', views.payment_failed, name='payment-failed'),

    path('my-orders', views.my_orders, name='my-orders'),

]


