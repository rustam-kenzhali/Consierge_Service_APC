from django.urls import path, re_path
# from django.views.decorators.cache import cache_page
from django.contrib.auth.views import auth_login
from main.views import *

urlpatterns = [
    # path('', cache_page(60)(PostHome.as_view()), name='home'),
    path('', MainPage.as_view(), name='main'),
    path('service/<slug:service_slug>/', ServicePage.as_view(), name='service'),
    path('service/<slug:service_slug>/<slug:partner_slug>/', OrderPage.as_view(), name='order'),
    path('payment/<order_id>/', PaymentPage, name='payment'),
    path('complete/', PaymentCompletePage, name='complete'),

    path('contacts/', ContactPage.as_view(), name='contacts'),
    path('profile/', ProfilePage.as_view(), name='profile'),

    path('', auth_login, name="login"),
    path('registration/', RegisterView.as_view(), name='reg'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('choose_service/', ChooseService.as_view(), name='choose'),

    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
