from rest_framework import serializers

from forum_app.models import Comment, Material, Vote


class VotesSerializer(serializers.Serializer):
    """
    Vote serializer mixin
    """

    votes_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    def get_votes_count(self, obj):
        return obj.votes.all().count()

    def get_likes_count(self, obj):
        return obj.votes.filter(type=Vote.TYPE_PLUS).count()

    def get_dislikes_count(self, obj):
        return obj.votes.filter(type=Vote.TYPE_MINUS).count()


class MaterialSerializer(serializers.ModelSerializer, VotesSerializer):

    class Meta:
        model = Material
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer, VotesSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
