import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from forum_app.models import Material, Vote


class VotesTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def _create_material(self, type):
        """
        Utility method for material creation
        :param type: material type
        """

        data = {
            'type': type,
            'title': 'test article title',
            'text': 'test article text',
            'author': 'author@forum.com'
        }
        response = self.client.post(reverse('material-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], 1)
        self.assertEqual(response_data['title'], data['title'])
        self.assertEqual(response_data['type'], data['type'])

    def _vote(self, material_pk, type, action, expected_response):
        """
        Utility method for vote createion
        :param material_pk: material pk
        :param type: vote type
        :param action: add/remove vote
        :param expected_response: expected message from response
        """

        if type == Vote.TYPE_PLUS:
            if action == 'add':
                url = reverse('material-like-add', args=[material_pk])
            else:
                url = reverse('material-like-remove', args=[material_pk])
        else:
            if action == 'add':
                url = reverse('material-dislike-add', args=[material_pk])
            else:
                url = reverse('material-dislike-remove', args=[material_pk])

        response = self.client.post(url, data={'user': 'user@forum.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], expected_response)

    def test_create_article(self):
        self._create_material(type=Material.TYPE_ARTICLE)

    def test_create_news(self):
        self._create_material(type=Material.TYPE_NEWS)

    def test_create_like(self):
        self._create_material(type=Material.TYPE_ARTICLE)
        article = Material.objects.filter(type=Material.TYPE_ARTICLE).first()
        self.assertTrue(article is not None)
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='Your vote is added', action='add')

    def test_create_like_twice(self):
        self._create_material(type=Material.TYPE_ARTICLE)
        article = Material.objects.filter(type=Material.TYPE_ARTICLE).first()
        self.assertTrue(article is not None)
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='Your vote is added', action='add')
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='You have already voted',
                   action='add')

    def test_create_like_and_then_dislike(self):
        self._create_material(type=Material.TYPE_ARTICLE)
        article = Material.objects.filter(type=Material.TYPE_ARTICLE).first()
        self.assertTrue(article is not None)
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='Your vote is added', action='add')
        self._vote(material_pk=article.pk, type=Vote.TYPE_MINUS, expected_response='You have already voted',
                   action='add')

    def test_replace_like_for_dislike(self):
        self._create_material(type=Material.TYPE_ARTICLE)
        article = Material.objects.filter(type=Material.TYPE_ARTICLE).first()
        self.assertTrue(article is not None)
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='Your vote is added', action='add')
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='Your vote is removed',
                   action='remove')
        self._vote(material_pk=article.pk, type=Vote.TYPE_MINUS, expected_response='Your vote is added', action='add')

    def test_remove_like_if_not_exist(self):
        self._create_material(type=Material.TYPE_ARTICLE)
        article = Material.objects.filter(type=Material.TYPE_ARTICLE).first()
        self.assertTrue(article is not None)
        self._vote(material_pk=article.pk, type=Vote.TYPE_PLUS, expected_response='Your did not vote', action='remove')
