from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from sold_house_prices import settings
from .serializers import SoldHouseSerializer
from .models import SoldHouse

from datetime import datetime


class SoldHouseViewSet(viewsets.ModelViewSet):
    queryset = SoldHouse.objects.all().order_by('tx_date')
    serializer_class = SoldHouseSerializer
    http_method_names = ['get', 'head']  # only allow GET and HEAD http methods


class SoldHouseAvgPriceViews(APIView):
    serializer_class = SoldHouseSerializer

    def get(self, request):
        post_code = self.request.GET.get('post_code')
        if post_code is None:
            post_code = settings.DEFAULT_POST_CODE

        from_date = self.request.GET.get('from_date')
        if from_date is None:
            from_date = settings.DEFAULT_FROM_DATE
        from_date_formatted = datetime.strptime(from_date, '%Y-%m').strftime('%Y-%m-%d')

        to_date = self.request.GET.get('to_date')
        if to_date is None:
            to_date = settings.DEFAULT_TO_DATE
        to_date_formatted = datetime.strptime(to_date, '%Y-%m')
        to_date_formatted = to_date.strftime('%Y-%m-28') if to_date_formatted.month == 2 \
            else to_date_formatted.strftime('%Y-%m-30')

        queryset = SoldHouse.objects.filter(post_code=post_code)
        queryset = queryset.filter(tx_date__gte=from_date_formatted)
        queryset = queryset.filter(tx_date__lte=to_date_formatted)

        serializer = SoldHouseSerializer(queryset, many=True)
        if serializer.data:
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        raise Http404


class SoldHouseTxNumberViews(APIView):
    serializer_class = SoldHouseSerializer

    def get(self, request):
        post_code = self.request.GET.get('post_code')
        queryset = SoldHouse.objects.all() if post_code is None else SoldHouse.objects.filter(post_code=post_code)

        date = self.request.GET.get('date')
        if date is None:
            date = settings.DEFAULT_DATE
        from_date = datetime.strptime(date, '%Y-%m').strftime('%Y-%m-%d')
        to_date = datetime.strptime(date, '%Y-%m')
        to_date = to_date.strftime('%Y-%m-28') if to_date.month == 2 else to_date.strftime('%Y-%m-30')

        queryset = queryset.filter(tx_date__gte=from_date)
        queryset = queryset.filter(tx_date__lte=to_date)

        serializer = SoldHouseSerializer(queryset, many=True)
        extracted_data = serializer.data
        print(extracted_data)

        histogram_dict = self.create_histogram_data(extracted_data)

        if serializer.data:
            return Response({"status": "success", "data": histogram_dict}, status=status.HTTP_200_OK)

        raise Http404

    @staticmethod
    def create_histogram_data(extracted_data):
        def get_tx_number_between(below_limit, upper_limit):
            count = 0
            for datum in extracted_data:
                if below_limit < datum.get('price_paid', 0) >= upper_limit:
                    count += 1
            return count

        price_paids = []
        min_price, max_price = 0, 0
        for extracted_datum in extracted_data:
            price_paids.append(extracted_datum.get('price_paid'))
        if price_paids:
            min_price, max_price = min(price_paids), max(price_paids)
        interval = int((max_price - min_price) / (settings.HISTOGRAM_BRACKET_NUMBER + 1))
        under_price_value = min_price + interval

        histogram_dict = {
            1: {'label': f'Under {under_price_value}', 'value': get_tx_number_between(0, under_price_value)},
            2: {'label': f'{under_price_value + interval * 0} - {under_price_value + interval * 1}',
                'value': get_tx_number_between(under_price_value + interval * 0, under_price_value + interval * 1)},
            3: {'label': f'{under_price_value + interval * 1} - {under_price_value + interval * 2}',
                'value': get_tx_number_between(under_price_value + interval * 1, under_price_value + interval * 2)},
            4: {'label': f'{under_price_value + interval * 2} - {under_price_value + interval * 3}',
                'value': get_tx_number_between(under_price_value + interval * 2, under_price_value + interval * 3)},
            5: {'label': f'{under_price_value + interval * 3} - {under_price_value + interval * 4}',
                'value': get_tx_number_between(under_price_value + interval * 3, under_price_value + interval * 4)},
            6: {'label': f'{under_price_value + interval * 4} - {under_price_value + interval * 5}',
                'value': get_tx_number_between(under_price_value + interval * 4, under_price_value + interval * 5)},
            7: {'label': f'{under_price_value + interval * 5} - {under_price_value + interval * 6}',
                'value': get_tx_number_between(under_price_value + interval * 5, under_price_value + interval * 6)},
            8: {'label': f'Over {under_price_value + interval * 6}',
                'value': get_tx_number_between(under_price_value + interval * 6, max_price)},
        }

        return histogram_dict
