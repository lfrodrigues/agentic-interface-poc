from django.db import models
from django.utils import timezone


class BillingAddress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}"


class User(models.Model):
    # User Profile Fields
    customer_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    account_status = models.CharField(max_length=50)
    registration_date = models.DateTimeField()

    # Subscription Fields
    plan_name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=50)
    subscription_start_date = models.DateTimeField()
    subscription_renewal_date = models.DateTimeField()
    auto_renewal = models.BooleanField(default=True)

    # Services Fields
    voice_enabled = models.BooleanField(default=True)
    data_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=True)
    roaming_enabled = models.BooleanField(default=True)

    # Billing Fields
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=50)
    billing_cycle = models.CharField(max_length=50)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['customer_id']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.user_id})"

    @classmethod
    def from_user_information(cls, user_data: dict):
        """
        Create or update a User instance from the get_user_information response
        """
        profile = user_data['user_profile']
        subscription = user_data['subscription']
        services = user_data['services']
        billing = user_data['billing']

        # Create or update billing address
        billing_address, _ = BillingAddress.objects.update_or_create(
            street=billing['billing_address']['street'],
            city=billing['billing_address']['city'],
            defaults={
                'state': billing['billing_address']['state'],
                'zip': billing['billing_address']['zip'],
                'country': billing['billing_address']['country'],
            }
        )

        # Create or update user
        user, created = cls.objects.update_or_create(
            customer_id = profile['customer_id'],
            defaults={
                'full_name': profile['full_name'],
                'email': profile['email'],
                'account_status': profile['account_status'],
                'registration_date': profile['registration_date'],
                'plan_name': subscription['plan_name'],
                'plan_type': subscription['plan_type'],
                'subscription_start_date': subscription['start_date'],
                'subscription_renewal_date': subscription['renewal_date'],
                'auto_renewal': subscription['auto_renewal'],
                'voice_enabled': services['voice'],
                'data_enabled': services['data'],
                'sms_enabled': services['sms'],
                'roaming_enabled': services['roaming'],
                'payment_method': billing['payment_method'],
                'billing_cycle': billing['billing_cycle'],
                'billing_address': billing_address,
            }
        )
        return user 