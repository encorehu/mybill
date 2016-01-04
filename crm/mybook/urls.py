from django.conf.urls import include, url
from mybook.views import BookIndexView
from mybook.views import BookDoView
from mybook.views import BookCategoryDoView

urlpatterns = [
    url(r'(?P<bookid>\d+)/bill.do', BookDoView.as_view()),
    url(r'(?P<bookid>\d+)/category.do', BookCategoryDoView.as_view()),
    url(r'(?P<bookid>\d+)/$', BookIndexView.as_view()),
    url(r'(?P<bookid>\d+)', BookIndexView.as_view()),
]
