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

        # Set the path to the invalid test file
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test_data_invalid.xlsx')

    def test_upload_file_with_validation_errors(self):
        with open(self.test_file_path, 'rb') as test_file:
            # Send a POST request to upload the test file
            response = self.client.post(self.url, {'file': test_file}, format='multipart')

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the expected message about validation errors
        self.assertIn('Validation errors found', response.data['message'])

        # Assert that the response contains the 'errors' key
        self.assertIn('errors', response.data)

        # Assert that the 'errors' list is not empty, indicating validation errors
        self.assertTrue(response.data['errors'])
