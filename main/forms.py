from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


# class RegisterUserForm(forms.ModelForm):
#     # username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input-field'}))
#     # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input-field'}))
#     # password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input-field'}))
#
#     class Meta:
#         model = CS_User
#         fields = ['username', 'email', 'password']
#
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'input-field', 'minlength': '4', 'autocomplete':'off', 'required':'required'}),
#             'email': forms.EmailInput(attrs={'class': 'input-field', 'minlength': '4', 'autocomplete':'off', 'required':'required'}),
#             'password': forms.PasswordInput(attrs={'class': 'input-field', 'minlength': '7', 'autocomplete':'off', 'required':'required'})
#         }
#
#
# class LoginUserForm(forms.ModelForm):
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input-field'}))
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input-field'}))
#
#     class Meta:
#         model = CS_User
#         fields = ['email', 'password']
#


class CustomUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input-field'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input-field'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input-field'}))

    class Meta:
        model = CS_User
        fields = ('email', 'username', 'password1', 'is_b2b')



    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        del self.fields['password2']


class PartnerSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cities_field'].empty_label = 'Категория не выбрана'

    SERVICE = [('Отель', 'Отель'), ('Авиаперелёты', 'Авиаперелёты'), ('Автотранспорт', 'Автотранспорт'),
               ('Яхты', 'Яхты')]
    CITIES = [('Астана', 'Астана'), ('Алматы', 'Алматы')]
    PRICE = [('10000 - 24999', '10000 - 24999'), ('25000 - 49999', '25000 - 49999'),
             ('50000 - 124999', '50000 - 124999'), ('125000 - 244999', '125000 - 244999'),
             ('250000 - 500000', '250000 - 500000')]

    cities_field = forms.ChoiceField(choices=CITIES)
    price_field = forms.ChoiceField(choices=PRICE)
    service_field = forms.ChoiceField(choices=SERVICE)

    # cities_field.widget.attrs.update({'class': 'form-select'})

    # class Meta:
    #     model = Service
    #     fields = ['title']
    #     widgets = {
    #         'title': forms.TextInput(attrs={'class': 'form-input'}),
    #     }
    #


class ContactForm(forms.Form):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Имя'}), max_length=255)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                                max_length=255)

    SERVICES = [('Отель', 'Отель'), ('Авиаперелёты', 'Авиаперелёты'), ('Автотранспорт', 'Автотранспорт'),
                ('Яхты', 'Яхты')]
    service_choice = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SERVICES,
    )

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Почта'}), max_length=255)

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'placeholder': 'Ваше сообщение...'}))


# class ChooseServiceForm(forms.Form):
#     SERVICES = []
#     for service in Service.objects.all():
#         SERVICES.append((service, service))
#
#     service_choice = forms.MultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         choices=SERVICES,
#     )


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('first_name', 'second_name', 'last_name', 'user_id_card', 'time_start', 'time_end','count', 'city', 'address', 'info')

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'second_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Отчество'}),
            'time_start': forms.TimeInput(attrs={'type': 'datetime-local'}),
            'time_end': forms.TimeInput(attrs={'type': 'datetime-local'}),

            'user_id_card': forms.FileInput(attrs={'class': 'input-file', 'id': 'my-file'}),

            'count': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Количество'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес'}),
            'info': forms.Textarea(attrs={'cols': 40, 'rows': 3, 'placeholder': 'Детализируйте ваш заказ'})
        }


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = CS_User
        fields = ('info', 'full_name', 'image', 'company_name', 'company_role', 'phone', 'address', 'facebook_link', 'instagram_link', 'twitter_link')

        widgets = {
            'info': forms.TextInput(attrs={'placeholder': 'Информация о себе', 'class': 'form-control profile_input'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Введите ваше фио', 'class': 'form-control profile_input'}),
            'image': forms.FileInput(attrs={'class': 'form-control profile_input', 'id': 'exampleInputPhoto'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Введите место вашей работы', 'class': 'form-control profile_input'}),
            'company_role': forms.TextInput(attrs={'placeholder': 'Введите вашу должность', 'class': 'form-control profile_input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Введите ваш номер', 'class': 'form-control profile_input'}),
            'address': forms.TextInput(attrs={'placeholder': 'Введите ваш адрес', 'class': 'form-control profile_input'}),

            'facebook_link': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш аккаунт', 'class': 'form-control profile_input'}),
            'instagram_link': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш аккаунт', 'class': 'form-control profile_input'}),
            'twitter_link': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш аккаунт', 'class': 'form-control profile_input'}),

        }