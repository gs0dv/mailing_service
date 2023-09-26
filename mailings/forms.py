from django import forms
from django.forms import BaseModelFormSet

from mailings.models import Mailing, Client
from mailings.services import get_active_user

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        # fields = '__all__'  # все поля
        # fields = ('first_name', 'last_name', 'avatar', 'email',)  # либо по полям
        exclude = ('status', 'owner',)  # исключение

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['clients'].queryset = Client.objects.filter(owner=get_active_user())
        # print(self.fields['clients'].queryset)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        # fields = '__all__'  # все поля
        # fields = ('first_name', 'last_name', 'avatar', 'email',)  # либо по полям
        # exclude = ('status',) # исключение
        exclude = ('owner',)
