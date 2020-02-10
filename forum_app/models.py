from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models


class Material(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    TYPE_ARTICLE = 0
    TYPE_NEWS = 1
    TYPES = (
        (TYPE_ARTICLE, 'Article'),
        (TYPE_NEWS, 'News')
    )
    type = models.PositiveSmallIntegerField(choices=TYPES, default=TYPE_ARTICLE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    publish_date = models.DateTimeField(blank=True, null=True)
    author = models.EmailField()
    votes = GenericRelation('Vote', related_query_name='material')

    def __str__(self):
        return self.title


class Comment(models.Model):

    material = models.ForeignKey(Material, related_name='comments', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    user = models.EmailField()
    votes = GenericRelation('Vote', related_query_name='comment')

    def __str__(self):
        return self.id


class Vote(models.Model):

    TYPE_PLUS = 0
    TYPE_MINUS = 1
    TYPES = (
        (TYPE_PLUS, 'Like'),
        (TYPE_MINUS, 'Dislike')
    )
    type = models.PositiveSmallIntegerField(choices=TYPES)
    user = models.EmailField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.id

    class Meta:
        unique_together = ('object_id', 'content_type', 'user')
