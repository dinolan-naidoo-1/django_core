from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import TransactionData
from datetime import datetime
from decimal import Decimal

class RetrieveRowsViewTestCase(APITestCase):
    def setUp(self):
        # Create sample data for testing
        TransactionData.objects.create(
            country='US',
            date=datetime.strptime('2024-05-21', '%Y-%m-%d').date(),
            transaction_type='Sale',
            currency='USD',
            net_amount=Decimal('100.00'),
            input_amount=Decimal('100.00')
        )

    def test_retrieve_rows_success(self):
        url = reverse('retrieveRows')
        params = {
            'country': 'US',
            'date': '2024/05/21',
            'currency': 'EUR'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting one row in the response
        self.assertEqual(response.data[0]['country'], 'US')
        self.assertEqual(response.data[0]['date'], '2024-05-21')
        self.assertEqual(response.data[0]['transaction_type'], 'Sale')
        self.assertEqual(response.data[0]['currency'], 'EUR')

    def test_retrieve_rows_no_content(self):
        url = reverse('retrieveRows')
        params = {
            'country': 'DE',
            'date': '2024/05/21',
            'currency': 'EUR'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_rows_invalid_date_format(self):
        url = reverse('retrieveRows')
        params = {
            'country': 'US',
            'date': '2024-05-21',  # Incorrect date format
            'currency': 'EUR'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

