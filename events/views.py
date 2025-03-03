# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from .models import Event, Ticket
from .serializers import UserSerializer, EventSerializer
from .permissions import EventsViewPermissions, TicketPurchasePermissions

User = get_user_model()

class UserRegisterView(APIView):
    """
    View to create a new user
    """
    renderer_classes = [JSONRenderer]

    def post(self, request):
        return Response({"message": "Use POST methodto register a user"}, status = status.HTTP_400_BAD_REQUEST)
    
    # Post method for user registration
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class EventsView(APIView):
    """
    Provides role-based access to get list of events or to create an event.
    """

    permission_classes = [EventsViewPermissions]
    renderer_classes = [JSONRenderer]

    
    def get(self, request):
        """
        To get list of events
        """
        # Fetch all events
        events = Event.objects.all()
        # Serialize events list
        serializer = EventSerializer(events, many = True)
        return Response(serializer.data)
    
    
    def post(self, request):
        """
            To create an event
        """
        # Serialize request data
        serializer = EventSerializer(data = request.data)
        # Validate request data against the model
        if serializer.is_valid():
            # Create an event object 
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TicketPurchaseView(APIView):
    """
    Allows 'User' role to purchase tickets. 
    This view has custom logic before creating an object therefore, 
    Serializer is not used here.
    """
    permission_classes = [TicketPurchasePermissions]
    renderer_classes = [JSONRenderer]
    
    def post(self, request, event_id):
        try:
            # Get the event object
            event = Event.objects.get(pk = event_id)
        except Event.DoesNotExist:
            # Return error if event object does not exist
            return Response({"error": "Purchasing for a non-existent event"}, 
            status=status.HTTP_400_BAD_REQUEST)
        quantity = request.data.get("quantity", 0)
        # Check if quantity is an integer and it is greater than 0
        if isinstance(quantity, int) and quantity > 0:
            # Total tickets should be greater or equal to tickets_sold and quantity
            if event.total_tickets >= (event.tickets_sold + quantity):
                Ticket.objects.create(
                    user = request.user,
                    event = event,
                    quantity = quantity)
                # Update event object
                event.tickets_sold += quantity
                event.save()
                return Response({"message": "Tickets Purchased Successully"}, status = status.HTTP_201_CREATED)
            return Response({"error": "Available tickets less than requested tickets"}, 
            status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid ticket quantity"}, 
            status=status.HTTP_400_BAD_REQUEST)
