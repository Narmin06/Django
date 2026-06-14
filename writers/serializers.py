from rest_framework import serializers

from .models import Writer


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['id', 'name', 'bio', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Name cannot be empty.')
        return value
