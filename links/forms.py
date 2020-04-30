from django import forms

import re

from .models import Link


class AdminLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class LinkForm(forms.ModelForm):

    RESTRICTED_VALUES = ["admin", "delete"]

    class Meta:
        model = Link
        fields = ["short_id", "destination"]

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