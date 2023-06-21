from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from core.models import Country

class CountryApiTest(APITestCase):
    def setUp(self):
        # Create test data in the PostgreSQL database
        Country.objects.create(country='Andorra', rank='37', amount='18.0', year='1987')
        # Create other test data as needed

    def test_get_country(self):
        url = reverse('country')  # Assuming you have a named URL for your CountryApiView
        response = self.client.get(url + '?country=Andorra')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        country_data = response.data[0]
        self.assertEqual(country_data['country'], 'Andorra')