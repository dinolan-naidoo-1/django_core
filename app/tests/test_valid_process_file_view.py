import os
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import TransactionData

class ProcessFileViewTest(TestCase):

    def setUp(self):
        """
        Set up the test case with necessary configurations.
        """
        # Initialize an APIClient instance
        self.client = APIClient()

        # Get the URL for the 'processFile' endpoint
        self.url = reverse('processFile')

        # Set the path to the valid test file
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test_data_valid.xlsx')

    def test_upload_valid_rows(self):
        with open(self.test_file_path, 'rb') as test_file:
            # Send a POST request to upload the test file
            response = self.client.post(self.url, {'file': test_file}, format='multipart')

        # Assert that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that 3 valid rows exist in the test_data_valid file
        self.assertEqual(TransactionData.objects.count(), 3)
