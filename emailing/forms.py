from django import forms

from emailing.models import Client, Emailing, Text_Messages


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'


class Text_MessagesForm(StyleFormMixin, forms.ModelForm):
    """Форма сообщения"""

    class Meta:
        model = Text_Messages
        fields = ["topic", "body", "owner"]


class EmailingForm(StyleFormMixin, forms.ModelForm):
    """Форма рассылки"""

    class Meta:
        model = Emailing
        exclude = ('emailing_owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Форма клиента"""

    class Meta:
        model = Client
        fields = ["full_name", "email", "description"]
