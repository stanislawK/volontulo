"""
.. module:: test_password_register
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
from django.test import Client

class TestUserRegister(TestCase):

    """ Tests for user register """

    def test_first_registration(self):
        """Test new user's registration"""
        response = self.client.post(
            reverse('register'),
            json.dumps({
                "email": "jannowak@o2.pl",
                "password": "jan123456"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_socond_registration(self):
        """Test register if user is registered already"""
        self.client = Client()
        self.client.login(
            username='volunteer2@example.com',
            password='volunteer2'
        )
        response = self.client.post(
            reverse('register'),
            json.dumps({
                "email": "volunteer2@example.com",
                "password": "volunteer2"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
