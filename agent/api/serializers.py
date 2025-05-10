from rest_framework import serializers
from agno2.models import User, Invoice, PaymentCard


class MessageInputSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    session_id = serializers.CharField(required=False)


class UserCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'issue_date', 'amount', 'status']


class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = ['card_number', 'expiration_date', 'payment_method_id']


class UserListSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)
    payment_cards = PaymentCardSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['customer_id', 'full_name', 'email', 'invoices', 'payment_cards']


class InvoiceCreateSerializer(serializers.Serializer):
    customer_id = serializers.CharField(required=True)
