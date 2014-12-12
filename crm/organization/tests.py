from django.utils import unittest
from django.test import TestCase
from django.test import Client

class SimpleTest(unittest.TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        self.client = Client()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    def test_login(self):
        c = Client()
        self.assertTrue(self.client.login(username='ravip',password='coriolis'))

class OrgListTestCase(TestCase):

    def test_index(self):
        resp = self.client.get('/org/list/')
        self.assertEqual(resp.status_code, 200)
