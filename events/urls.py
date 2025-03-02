from django.urls import path
from .views import UserRegisterView, EventsView, TicketPurchaseView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'user-register'),
    path('events/', EventsView.as_view(), name = 'events'),
    path('events/<int:event_id>/purchase/', TicketPurchaseView.as_view(), name = 'purchase')
]