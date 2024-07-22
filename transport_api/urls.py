from django.urls import path,include
from .views import bus_agencyView,routesView,AgencyBasedBusesView,RouteBasedBusesView,BookingView
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('agencies/',bus_agencyView.as_view(),name='agencies'),
    path('routes/',routesView.as_view(),name='routes'),
    path('agency-buses/<int:id>/',AgencyBasedBusesView.as_view()),
    path('route-buses/<int:id>/',RouteBasedBusesView.as_view()),
    path('bookings/', BookingView.as_view(), name='booking-create'),

    
]
