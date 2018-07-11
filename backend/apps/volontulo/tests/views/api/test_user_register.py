"""
.. module:: test_password_reset
"""

import json
from unittest import mock
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from apps.volontulo.factories import UserFactory
from apps.volontulo.views.api import register_view
from django.urls import reverse


class TestUserRegister(TestCase):

    """ Tests for user register """

    def setUp(self):
        """ Set up for each test """
        self.user = UserFactory.create()
        self.uid = str(
            urlsafe_base64_encode(force_bytes(self.user.pk)),
            'utf-8')
        self.token = default_token_generator.make_token(self.user)

    def test_registration_view_get(self):
        """GET to the register view"""
        response = self.client.get('/api/register/')
        self.assertEqual(response.status_code, 200)

    # def test_first_registration(self):
    #     """Test new user's registration"""
    #     response = self.client.post('/api/register/',
    #     user={
    #     'email': 'jankowalski@o2.pl',
    #     'password': 'jan123',
    #     "checkboxTA": "accept"
    #     })
    #     self.assertEqual(response.status_code, 201)

    # def test_first_registration(self):
    #     """Test new user's registration"""
    #     # new_user = self.user
    #     new_user = User.objects.create_user(
    #                 username="jankowalski@o2.pl",
    #                 email="jankowalski@o2.pl",
    #                 password='jan123',
    #                 is_active=False,
    #             )
    #     response = self.client.post('/api/register/', user=new_user)
    #     self.assertEqual(response.status_code, 201)
