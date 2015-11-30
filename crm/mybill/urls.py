from django.conf.urls import include, url
from mybill.views import BillIndexView

urlpatterns = [
    url(r'$', BillIndexView.as_view()),
]
