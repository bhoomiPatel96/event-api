from rest_framework.permissions import BasePermission

class EventsViewPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET': # Allow all authenticated users to fetch events
            return request.user.is_authenticated
        elif request.method == 'POST':  # Allow only admin users to post events
            return request.user.is_authenticated and getattr(request.user, 'role', None) == 'Admin'
        return False  # Access denied

class TicketPurchasePermissions(BasePermission):
    def has_permission(self, request, view):
        # Only 'User' can buy tickets
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'User'