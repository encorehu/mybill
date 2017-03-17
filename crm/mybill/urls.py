from django.conf.urls import include, url
from mybill.views import BillIndexView
from mybill.views import BillDoView
from mybill.views import BillCategoryDoView
from mybill.views import BillAccountDoView
from mybill.views import BillAccountBookDoView

urlpatterns = [
    url(r'accountbook.do', BillAccountBookDoView.as_view()),
    url(r'account.do', BillAccountDoView.as_view()),
    url(r'bill.do', BillDoView.as_view()),
    url(r'category.do', BillCategoryDoView.as_view()),
    url(r'$', BillIndexView.as_view()),
]
