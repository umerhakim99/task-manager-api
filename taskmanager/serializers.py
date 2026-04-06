from rest_framework import serializers
from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def validate(self, data):

        # Title validation
        title = data.get('title')
        if title is not None and len(title) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long"
            )

        # Deadline validation
        from datetime import date
        deadline = data.get('deadline')
        if deadline and deadline < date.today():
            raise serializers.ValidationError(
                "Deadline cannot be in the past"
            )

        return data