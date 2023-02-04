import json

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.views.generic import ListView, DeleteView, CreateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import auth_login
from django.contrib.auth import get_user_model


from .forms import *
from .tokens import account_activation_token
from .utils import take_kzt_to_usd

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


# from .utils import *
class MainPage(FormView):
    form_class = PartnerSearchForm
    template_name = 'main/main.html'

    # success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('main')


class ContactPage(FormView):
    form_class = ContactForm
    template_name = 'main/contacts.html'

    # success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('main')


class ChooseService(View):
    model = Service
    template_name = 'main/choose_service.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'services': Service.objects.all()})


    def post(self, request, *args, **kwargs):
        form = request.POST.getlist("checkbox_service")
        user = CS_User.objects.get(pk=self.request.user.pk)

        for i in form:
            user.services.add(Service.objects.get(pk=i))

        user.save()

        return redirect('main')

    # def form_valid(self, form):
    #     print(self.request.POST.get("checkbox_service"))
    #     return redirect('choose')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('choose')

    return redirect('main')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate user account'
    html_content = render_to_string("main/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }
                               )

    text_content = strip_tags(html_content)

    # email = EmailMessage(mail_subject, plain_message, to=[to_email])
    email = EmailMultiAlternatives(mail_subject, text_content, to=[to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

    # if email.send():
    #     # message.success(request, f'Dear <b>{user}</b>, please go to email <b>{email}</b> ')
    #     print('SUCCES')
    # else:
    #     # message.error(request, f'Problem sending email to {to_email}, check if you typed it correctly go to email and success it')
    #     print('ERROR')

class RegisterView(CreateView):
    form_class = CustomUserForm
    form_name = "Test"
    success_url = reverse_lazy('main')
    template_name = 'registration/reg.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        activateEmail(self.request, user, form.cleaned_data.get('email'))
        return redirect('main')


class ServicePage(ListView):
    model = Service_category
    form_class = PartnerSearchForm
    template_name = 'main/service.html'
    context_object_name = 'service_category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        service = Service.objects.get(slug=self.kwargs['service_slug'])
        context['service_bg'] = service.bg_img
        return context

    def get_queryset(self):
        return Service_category.objects.filter(service__slug=self.kwargs['service_slug'])


def PaymentCompletePage(request):
    # try:
    body = json.loads(request.body)
    order = Order.objects.get(pk=body['orderID'])
    order.is_active = True
    order.save()
    # print('Body: ', body)
    # print(body)
    return JsonResponse({})
    #
    # except:
    #     print('not work')


def PaymentPage(request, order_id):
    usd = take_kzt_to_usd(order_id)
    return render(request, 'main/payment.html', {'order': Order.objects.get(pk=order_id), 'price': usd})


class OrderPage(LoginRequiredMixin, CreateView):
    template_name = 'main/order.html'
    model = Partners
    form_class = OrderForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        order = form.save(commit=False)
        order.userID = self.request.user.pk
        order.username = self.request.user.username
        order.item = Partners.objects.get(slug=self.request.path.split('/')[3])
        order.save()
        return redirect('payment', order_id = order.pk)





class ProfilePage(LoginRequiredMixin, View):
    model = CS_User
    template_name = 'main/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user_orders': Order.objects.filter(username=self.request.user.username), 'top_partners': Partners.objects.all()})


def archive(request, year):
    if int(year) > 2020:
        # raise Http404()
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Noob, page does not exit</h1>')
