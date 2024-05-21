from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from datetime import datetime
from ..models import TransactionData
from decimal import Decimal
import random

def mock_currency_conversion(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    conversion_rate = Decimal(random.uniform(0.5, 1.5)).quantize(Decimal('0.01'))
    return (amount * conversion_rate).quantize(Decimal('0.01'))

class RetrieveRowsView(APIView):

    def get(self, request):
        country = request.query_params.get('country')
        date_str = request.query_params.get('date')
        currency = request.query_params.get('currency')

        if not country or not date_str:
            return Response({
                'message': 'Country and date parameters are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Manually parse the date in YYYY/MM/DD as per the example format
            try:
                date = datetime.strptime(date_str, '%Y/%m/%d').date()
            except ValueError:
                return Response({
                    'message': 'Invalid date format. Use YYYY/MM/DD'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the data from the database
            queryset = TransactionData.objects.filter(country=country, date=date)

            if currency:
                data = [
                    {
                        'date': row.date,
                        'country': row.country,
                        'transaction_type': row.transaction_type,
                        'currency': currency,
                        'net_amount': mock_currency_conversion(row.net_amount, row.currency, currency),
                        'input_amount': mock_currency_conversion(row.input_amount, row.currency, currency),
                    }
                    for row in queryset
                ]
            else:
                data = list(queryset.values())

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

