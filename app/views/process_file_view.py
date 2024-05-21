from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from datetime import datetime

from ..serializers import TransactionSerializer
from ..models import TransactionData

class ProcessFileView(APIView):
    serializer_class = TransactionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({'message': 'File not valid'}, status=status.HTTP_400_BAD_REQUEST)

            excel_file = data.get('file')
            if not excel_file:
                return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(excel_file, sheet_name=0)
            data_array, errors = self.validate_data(df)

            if errors:
                return Response({'message': 'Validation errors found', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            TransactionData.objects.bulk_create(data_array)
            return Response({'message': 'Successfully uploaded data'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': 'Server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def validate_data(self, df):
        data_array = []
        errors = []

        for index, row in df.iterrows():
            row_errors = {}

            date = row['Date']
            country = row['Country']
            transaction_type = row['Transaction']
            currency = row['Currency']
            input_amount = row['Input Amount']
            net_amount = row['Net Amount']

            # Filter out data that does not contain the year 2020
            if not isinstance(date, datetime) or date.year != 2020:
                continue

            # Validations
            if not isinstance(date, datetime):
                row_errors['date'] = 'Invalid date format'
            if len(country) != 2:
                row_errors['country'] = 'Country code must be ISO 3166 format'
            if transaction_type not in ['purchase', 'sale']:
                row_errors['transaction_type'] = 'Transaction type must be purchase or sale'
            if len(currency) != 3:
                row_errors['currency'] = 'Currency code must be ISO 4217 format'
            if not isinstance(net_amount, (int, float)):
                row_errors['net_amount'] = 'Net amount must be a number'
            if not isinstance(input_amount, (int, float)):
                row_errors['input_amount'] = 'Input amount must be a number'

            if row_errors:
                errors.append({'row': index, 'errors': row_errors})
                continue

            input_data = TransactionData(
                date=date,
                country=country,
                transaction_type=transaction_type,
                currency=currency,
                input_amount=input_amount,
                net_amount=net_amount
            )
            data_array.append(input_data)

        return data_array, errors
