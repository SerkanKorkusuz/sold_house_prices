from django.core.management.base import BaseCommand

import csv
import datetime
import os
import yaml


# Management command for Windows OS:
# python manage.py create_initial_data --csv_file=pp-complete.csv --out_file=.\api_service\fixtures\pp-initial.yaml
class Command(BaseCommand):
    help = 'Creates initial fixture data for sold houses'

    @staticmethod
    def convert_to_yaml(line, counter):
        tx_date = datetime.datetime.strptime(line[2], '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
        new_build = True if line[5] == 'Y' else False
        item = {
            'model': 'api_service.SoldHouse',
            'pk': counter,
            'fields': {
                'tx_id': line[0],
                'price_paid': int(line[1]),
                'tx_date': tx_date,
                'post_code': line[3],
                'property_type': line[4],
                'new_build': new_build,
                'estate_type': line[6],
                'paon': line[7],
                'saon': line[8],
                'street': line[9],
                'locality': line[10],
                'town': line[11],
                'district': line[12],
                'county': line[13],
                'record_status': line[14]
            },
        }
        return item

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', help='Path of the source csv file to convert into yaml file')
        parser.add_argument('--out_file', help='Path of the output yaml file')

    def handle(self, *args, **kwargs):
        if not (os.path.exists(kwargs['out_file']) and os.stat(kwargs['out_file']).st_size):
            csv_file = open(kwargs['csv_file'], 'r')
            out_file = open(kwargs['out_file'], 'w')
            try:
                reader = csv.reader(csv_file)
                next(reader)
                for count, line_num in enumerate(reader):
                    item = self.convert_to_yaml(line_num, count + 1)
                    out_file.write(yaml.dump([item], default_flow_style=False))
            finally:
                csv_file.close()
                out_file.close()
