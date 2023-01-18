from django.urls import path, re_path
# from django.views.decorators.cache import cache_page

from main.views import *

urlpatterns = [
    # path('', cache_page(60)(PostHome.as_view()), name='home'),
    path('', MainPage.as_view(), name='main'),
    path('contacts/', ContactPage.as_view(), name='contact'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
