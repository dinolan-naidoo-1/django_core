from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
from ..models import TransactionData
from decimal import Decimal
import random

# Note on the actual API request, better error handling can be implemented with a proper API call to the European Central Bank
# For this demo, the mock functions are used as a replacement

def mock_currency_conversion(amount, conversion_rate):
    return (amount * conversion_rate).quantize(Decimal('0.01'))

def get_conversion_rate(queryset, currency):
    # If currency is provided and differs from row currency, generate a random conversion rate
    if currency:
        if queryset and queryset[0].currency != currency:
            conversion_rate = Decimal(random.uniform(0.5, 1.5)).quantize(Decimal('0.01'))
            return conversion_rate
    # Return default conversion rate if same currency is requested
    return Decimal(1.0)

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
            queryset = TransactionData.objects.filter(country=country, date=date).all()

            if not queryset:
                return Response({
                    'message': 'No items found for the specified date and country',
                }, status=status.HTTP_204_NO_CONTENT)

            # Get conversion rate
            conversion_rate = get_conversion_rate(queryset, currency)

            # Prepare response data
            data = []
            for row in queryset:
                net_amount = row.net_amount
                input_amount = row.input_amount
                if currency:
                    net_amount = mock_currency_conversion(net_amount, conversion_rate)
                    input_amount = mock_currency_conversion(input_amount, conversion_rate)
                data.append({
                    'id': row.id,
                    'date': row.date.strftime('%Y-%m-%d'),
                    'country': row.country,
                    'transaction_type': row.transaction_type,
                    'currency': currency or row.currency,
                    'net_amount': Decimal(net_amount),
                    'input_amount': Decimal(input_amount),
                })

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
