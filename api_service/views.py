from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from sold_house_prices import settings
from .serializers import SoldHouseSerializer
from .models import SoldHouse

from datetime import datetime, timedelta


class SoldHouseViewSet(viewsets.ModelViewSet):
    queryset = SoldHouse.objects.all().order_by('tx_date')
    serializer_class = SoldHouseSerializer
    http_method_names = ['get', 'head']  # only allow GET and HEAD http methods


class SoldHouseAvgPriceViews(APIView):
    serializer_class = SoldHouseSerializer

    def get(self, request):
        post_code = request.GET.get('post_code')
        queryset = SoldHouse.objects.all() if post_code is None else SoldHouse.objects.filter(post_code=post_code)

        from_date = request.GET.get('from_date')
        if from_date is None:
            from_date = settings.DEFAULT_FROM_DATE
        from_date_formatted = datetime.strptime(from_date, '%Y-%m').strftime('%Y-%m-%d')

        to_date = request.GET.get('to_date')
        if to_date is None:
            to_date = settings.DEFAULT_TO_DATE
        to_date_formatted = datetime.strptime(to_date, '%Y-%m')
        to_date_formatted = to_date_formatted.strftime('%Y-%m-28') if to_date_formatted.month == 2 \
            else to_date_formatted.strftime('%Y-%m-30')

        queryset = queryset.filter(tx_date__gte=from_date_formatted)
        queryset = queryset.filter(tx_date__lte=to_date_formatted)

        queryset_detached = queryset.filter(property_type=settings.PROPERTY_TYPES.get('Detached'))
        queryset_semi_detached = queryset.filter(property_type=settings.PROPERTY_TYPES.get('Semi detached'))
        queryset_terraced = queryset.filter(property_type=settings.PROPERTY_TYPES.get('Terraced'))
        queryset_flats = queryset.filter(property_type=settings.PROPERTY_TYPES.get('Flats'))

        detached_data = SoldHouseSerializer(queryset_detached, many=True).data
        semi_detached_data = SoldHouseSerializer(queryset_semi_detached, many=True).data
        terraced_data = SoldHouseSerializer(queryset_terraced, many=True).data
        flats_data = SoldHouseSerializer(queryset_flats, many=True).data

        total_data = {
            'D': detached_data,
            'S': semi_detached_data,
            'T': terraced_data,
            'F': flats_data,
        }

        price_over_time = self.calculate_avg_price_data_by_property_over_time(from_date_formatted,
                                                                              to_date_formatted,
                                                                              total_data)
        serializer = SoldHouseSerializer(queryset, many=True)
        if serializer.data:
            return Response({'status': 'success', 'data': price_over_time}, status=status.HTTP_200_OK)

        raise Http404

    def calculate_avg_price_data_by_property_over_time(self, from_date_formatted, to_date_formatted, total_data):
        from_date = datetime.strptime(from_date_formatted, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_formatted, '%Y-%m-%d')
        daily_delta = timedelta(days=1)

        price_over_time = []
        while from_date <= to_date:
            search_date = from_date.strftime("%Y-%m-%d")
            date_event = {
                'tx_date': search_date,
                'D': {'count': 0, 'summed_price': 0, 'avg_price': None},  # None : Not Applicable when it has no value
                'S': {'count': 0, 'summed_price': 0, 'avg_price': None},
                'T': {'count': 0, 'summed_price': 0, 'avg_price': None},
                'F': {'count': 0, 'summed_price': 0, 'avg_price': None},
            }
            self.update_price_over_time(date_event, total_data)
            price_over_time.append(date_event)
            from_date += daily_delta

        return price_over_time

    @staticmethod
    def update_price_over_time(date_event, total_data):
        def update_over_total_data(p_type):
            for detached_datum in total_data.get(p_type):
                if detached_datum.get('tx_date') == date_event.get('tx_date'):
                    date_event[p_type]['summed_price'] += float(detached_datum.get('price_paid'))
                    date_event[p_type]['count'] += 1

        for property_type in settings.PROPERTY_TYPES.values():
            update_over_total_data(property_type)
            tx_count = date_event.get(property_type, {}).get('count')
            if tx_count:
                date_event[property_type]['avg_price'] = \
                    date_event.get(property_type, {}).get('summed_price', 0) // tx_count
            date_event.get(property_type, {}).pop('summed_price')
            date_event.get(property_type, {}).pop('count')


class SoldHouseTxNumberViews(APIView):
    serializer_class = SoldHouseSerializer

    def get(self, request):
        post_code = request.GET.get('post_code')
        queryset = SoldHouse.objects.all() if post_code is None else SoldHouse.objects.filter(post_code=post_code)

        date = request.GET.get('date')
        if date is None:
            date = settings.DEFAULT_DATE
        from_date = datetime.strptime(date, '%Y-%m').strftime('%Y-%m-%d')
        to_date = datetime.strptime(date, '%Y-%m')
        to_date = to_date.strftime('%Y-%m-28') if to_date.month == 2 else to_date.strftime('%Y-%m-30')

        queryset = queryset.filter(tx_date__gte=from_date)
        queryset = queryset.filter(tx_date__lte=to_date)

        serializer = SoldHouseSerializer(queryset, many=True)
        extracted_data = serializer.data

        histogram_dict = self.create_histogram_data(extracted_data)

        if extracted_data:
            return Response({'status': 'success', 'data': histogram_dict}, status=status.HTTP_200_OK)

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
