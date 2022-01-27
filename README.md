## Backend Code Challenge

This work up is intended to show a broad array of topics of the backend technologies. It is also aimed to create and build APIs to support the front-end part.
## Remarks

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.
```bash
pip install -r requirements.txt
```
- Create an ``.env`` file inside the ``.\sold_house_prices`` directory and it must include the variables of the postgresql credientials and django admin user:
  ``DATABASE_USER``, ``DATABASE_PASSWORD``, ``DATABASE_NAME``, ``DATABASE_HOST``, ``DATABASE_PORT``, ``DJANGO_SUPERUSER_USERNAME``, ``DJANGO_SUPERUSER_EMAIL`` and ``DJANGO_SUPERUSER_PASSWORD`` .
- Another way to set environment variables can be done by exporting or setting them on the operating system
- The solution is already configured to be hosted on heroku and API links can be listed as:
  - ``https://sold-house-prices.herokuapp.com/api/sold-houses/avg-prices?post_code=<post_code>&from_date=<from_date>&to_date=<to_date>``
  - ``https://sold-house-prices.herokuapp.com/api/sold-houses/tx-numbers?post_code=<post_code>&date=<to_date>``
- Example requests: 
   - ``curl -X GET "https://sold-house-prices.herokuapp.com/api/sold-houses/avg-prices?post_code=BS20%206JQ&from_date=1994-01&to_date=2018-11"``
   - ``curl -X GET "https://sold-house-prices.herokuapp.com/api/sold-houses/tx-numbers?post_code=BS20%206JQ&date=2000-06"``
- The query parameters ``from_date``, ``to_date`` and ``date`` should be in the format of YYYY-MM as it is how used in the example requests.
- The query parameter ``post_code`` should be paid attention because it could contain a blank character that corresponds ``%20`` on the uri.
- There are three management commands to be used:
  - ``python manage.py check_superuser --username=${DJANGO_SUPERUSER_USERNAME} --email=${DJANGO_SUPERUSER_EMAIL} --password=${DJANGO_SUPERUSER_PASSWORD}`` (to check and create a superuser non-interactively if it does not exist)
  - ``python manage.py create_initial_data --csv_file=pp-complete.csv --out_file=.\api_service\fixtures\pp-initial.yaml`` (to create an initial loaddata from the single csv file)
  - ``python manage.py insert_initial_data --csv_file=pp-complete.csv`` (to insert initial csv data to the database table for sold houses by using Django ORM)
- The file ``pp-complete.csv`` should be downloaded from the data source [https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#single-file](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#single-file) and teh file should be located on the project root directory.

## Contact
Pull requests are welcome. You can also email to korkusuzs18@itu.edu.tr
