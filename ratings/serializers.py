from rest_framework import serializers

from movies.models import Movie

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Rating
        fields = [
            'id', 'user', 'movie', 'score', 'comment',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Score must be between 1 and 10.')
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        # 'movie' is absent on partial updates; fall back to the instance.
        movie = attrs.get('movie') or getattr(self.instance, 'movie', None)

        if user and movie and self.instance is None:
            if Rating.objects.filter(user=user, movie=movie).exists():
                raise serializers.ValidationError(
                    'You have already rated this movie. Update your rating instead.'
                )
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
