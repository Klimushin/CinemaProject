from rest_framework import generics, viewsets, permissions

from api.serializers import CustomerSerializer, HallSerializer, SessionSerializer, TicketSerializer
from cinema.models import Hall, Session, Ticket
from user.models import Customer


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    http_method_names = ['post', 'put', 'patch']
    permission_classes = [permissions.IsAdminUser]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    http_method_names = ['get', 'post', 'put', 'patch']


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]
