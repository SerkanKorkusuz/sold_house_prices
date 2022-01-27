from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from api_service.models import SoldHouse

from datetime import datetime

import csv
import os


# Management command utilising Django ORM:
# python manage.py insert_initial_data --csv_file=pp-complete.csv
class Command(BaseCommand):
    help = 'Inserts initial csv data to the database table for sold houses'

    @staticmethod
    def insert_to_db(row):
        tx_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
        new_build = True if row[5] == 'Y' else False
        SoldHouse.objects.create(tx_id=row[0], price_paid=int(row[1]), tx_date=tx_date,
                                 post_code=row[3], property_type=row[4], new_build=new_build,
                                 estate_type=row[6], paon=row[7], saon=row[8], street=row[9],
                                 locality=row[10], town=row[11], district=row[12],
                                 county=row[13], record_status=row[14])

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', help='Path of the source csv file to insert into the database table')

    def handle(self, *args, **kwargs):
        if os.path.exists(kwargs['csv_file']) and os.stat(kwargs['csv_file']).st_size:
            csv_file = open(kwargs['csv_file'], 'r')
            try:
                rows = csv.reader(csv_file)
                next(rows)
                for row in rows:
                    try:
                        self.insert_to_db(row)
                    except IntegrityError:  # Continue to insert next row after encountering a duplicated data
                        continue
            finally:
                csv_file.close()
