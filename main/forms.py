from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

class PartnerSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cities_field'].empty_label = 'Категория не выбрана'

    SERVICE = [('Отель', 'Отель'), ('Авиаперелёты', 'Авиаперелёты'), ('Автотранспорт', 'Автотранспорт'), ('Яхты', 'Яхты')]
    CITIES = [('Астана', 'Астана'), ('Алматы', 'Алматы')]
    PRICE = [('10000 - 24999', '10000 - 24999'), ('25000 - 49999', '25000 - 49999'), ('50000 - 124999', '50000 - 124999'), ('125000 - 244999', '125000 - 244999'), ('250000 - 500000', '250000 - 500000')]

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
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}), max_length=255)

    SERVICES = [('Отель', 'Отель'), ('Авиаперелёты', 'Авиаперелёты'), ('Автотранспорт', 'Автотранспорт'), ('Яхты', 'Яхты')]
    service_choice = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SERVICES,
    )

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Почта'}), max_length=255)

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'placeholder': 'Ваше сообщение...'}))

# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Контент')
#     is_published = forms.BooleanField(label='Публикации', required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(),
#     label='Категории', empty_label='Категория не выбрана')



