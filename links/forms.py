from django import forms

import re

from .models import Link
from .utils import get_random_short_id


class AdminLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class LinkForm(forms.ModelForm):

    RESTRICTED_VALUES = ["admin", "delete"]

    class Meta:
        model = Link
        fields = ["title", "destination"]

    def save(self, commit=True):
        instance = super(LinkForm, self).save(commit=False)
        instance.short_id = get_random_short_id()
        if commit:
            instance.save()
        return instance

    def clean_short_id(self):
        data = self.cleaned_data['short_id']

        if data in self.RESTRICTED_VALUES:
            raise ValidationError(
                _("Invalid short ID: %(value)s"),
                code="invalid",
                params={"value": data},
            )
        elif not re.match("^\w+$", data):
            raise ValidationError(
                _("Invalid short ID: %(value)s"),
                code="invalid",
                params={"value": data},
            )

        return data