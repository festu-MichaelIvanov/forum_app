from django.db import IntegrityError
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from forum_app.models import Comment, Material, Vote
from forum_app.rest_serializers import CommentSerializer, MaterialSerializer


class VoteViewSet(viewsets.ModelViewSet):

    def _vote_add(self, data, type, obj):
        """
        Utility method for add vote
        :param data: data from request
        :param type: vote type - like/dislike
        :param obj: new, article, comment
        :return: status
        """

        if 'user' not in data:
            message = 'Missed required param "user"'
            return message

        try:
            obj.votes.create(type=type, user=data['user'])
        except IntegrityError:
            message = 'You have already voted'
            return message

        message = 'Your vote is added'
        return message

    def _vote_remove(self, data, type, obj):
        """
        Utility method for remove vote
        :param data: data from request
        :param type: vote type - like/dislike
        :param obj: new, article, comment
        :return: status
        """

        if 'user' not in data:
            message = 'Missed required param "user"'
            return message

        dislike = obj.votes.filter(type=type, user=data['user']).first()

        if dislike is None:
            message = 'Your did not vote'
            return message

        dislike.delete()

        message = 'Your vote is removed'
        return message

    @action(detail=True, methods=['POST'], url_path='like-add', url_name='like-add')
    def like_add(self, request, pk=None):
        message = self._vote_add(data=request.data, type=Vote.TYPE_PLUS, obj=self.get_object())
        return Response({'message': message})

    @action(detail=True, methods=['POST'], url_path='like-remove', url_name='like-remove')
    def like_remove(self, request, pk=None):
        message = self._vote_remove(data=request.data, type=Vote.TYPE_PLUS, obj=self.get_object())
        return Response({'message': message})

    @action(detail=True, methods=['POST'], url_path='dislike-add', url_name='dislike-add')
    def dislike_add(self, request, pk=None):
        message = self._vote_add(data=request.data, type=Vote.TYPE_MINUS, obj=self.get_object())
        return Response({'message': message})

    @action(detail=True, methods=['POST'], url_path='dislike-remove', url_name='dislike-remove')
    def dislike_remove(self, request, pk=None):
        message = self._vote_remove(data=request.data, type=Vote.TYPE_MINUS, obj=self.get_object())
        return Response({'message': message})


class MaterialViewSet(VoteViewSet):

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class CommentViewSet(VoteViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
