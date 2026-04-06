from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def validate(self, data):

        # Message validation
        if len(data.get('message', '')) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long"
            )

        # Email unique check — skip current record on UPDATE
        instance = self.instance  # None = create, Object = update
        email = data.get('email')
        qs = Contact.objects.filter(email=email)

        if instance:
            qs = qs.exclude(pk=instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "This email is already used"
            )

        return data