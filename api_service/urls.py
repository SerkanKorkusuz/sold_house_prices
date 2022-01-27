from django.urls import include, path
from rest_framework import routers
from .views import SoldHouseViewSet, SoldHouseAvgPriceViews, SoldHouseTxNumberViews


router = routers.DefaultRouter()
router.register(r'sold_houses', SoldHouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sold-houses/avg-prices', SoldHouseAvgPriceViews.as_view()),
    path('sold-houses/tx-numbers', SoldHouseTxNumberViews.as_view()),
]

# curl -X GET "http://127.0.0.1:8000/api/sold-houses/avg-prices?post_code=BS20%206JQ&from_date=1999-10&to_date=2007-11"
# curl -X GET "http://127.0.0.1:8000/api/sold-houses/tx-numbers?post_code=BS20%206JQ&date=2000-06"
# curl -X GET "http://127.0.0.1:8000/api/sold-houses/tx-numbers?date=2000-06"
