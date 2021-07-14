from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from user.models import Customer
from cinema.models import Hall, Session, Ticket


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Customer
        fields = ('id', 'username', 'password', 'password2',)
        read_only = ('id', 'balance')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password mismatch')
        return data

    def create(self, validated_data):
        user = Customer.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = ('username', 'password')


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        read_only = ('id',)


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = (
            'id', 'hall', 'start_time', 'end_time', 'start_date', 'end_date',
            'price', 'status',
        )
        read_only = ('id', 'show_date', 'status')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
