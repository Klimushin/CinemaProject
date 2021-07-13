from rest_framework import serializers
from user.models import Customer
from cinema.models import Hall, Session, Ticket


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # fields = ('id', 'username', 'password', 'password2')
        # read_only = ('id', 'balance')


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        # fields = ('id', 'name', 'size')
        # read_only = ('id',)


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        # fields = (
        #     'id', 'hall', 'start_time', 'end_time', 'start_date', 'end_date',
        #     'show_date', 'price', 'status', 'free_places'
        # )
        # read_only = ('id', 'show_date', 'status')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
