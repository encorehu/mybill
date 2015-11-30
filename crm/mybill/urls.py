from django.conf.urls import include, url
from mybill.views import BillIndexView
from mybill.views import BillDoView
from mybill.views import BillCategoryDoView

urlpatterns = [
    url(r'bill.do', BillDoView.as_view()),
    url(r'category.do', BillCategoryDoView.as_view()),
    url(r'$', BillIndexView.as_view()),
]
