from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    path('offers/', views.offers, name='offers'),
    path('offers/<city>/<arrival>/<departure>/<people>/', views.offers, name='offers_city'),
    path('offers/<city>/<arrival>/<departure>/<people>/<orderby>/', views.offers, name='offers_orderby'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<city>/', views.favorites, name='favorite'),
    path('travel_history/', views.travel_history, name='travel_history'),
    path('hotel/', views.hotel, name='hotel'),
    path('hotel/<id_hotel_id>/', views.hotel, name='hotel_id'),
    path('hotel/<id_hotel_id>/<arrival>/<departure>/<people>/', views.hotel, name='hotel_id_hotel'),
    path('make_an_order/', views.order, name='order'),
    path('make_an_order/<id_room>/<arrival>/<departure>/<people>/', views.order, name='order_add'),
    path('payment/', views.payments, name='payment'),
    path('payment/<id_room>/<arrival>/<departure>/<people>/', views.payments, name='payment_new'),
    # path('successful_payment/', views.successful_payment, name='succefilly'),
    path('logout/', LogoutView.as_view(), name='logout'),
]