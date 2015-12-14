from django.conf.urls import include, url
from mybill.views import BillIndexView
from mybill.views import BillDoView
from mybill.views import BillCategoryDoView

urlpatterns = [
    url(r'(?P<accountid>\d+)/bill.do', BillDoView.as_view()),
    url(r'(?P<accountid>\d+)/category.do', BillCategoryDoView.as_view()),
    url(r'(?P<accountid>\d+)/$', BillIndexView.as_view()),
]
