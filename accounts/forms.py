
import re

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.db.models import Q

User = get_user_model()


class RegisterForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "First Name",
            "autocomplete": "given-name",
        }),
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Last Name",
            "autocomplete": "family-name",
        }),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "autocomplete": "email",
        }),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "autocomplete": "new-password",
        }),
        strip=False,
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "autocomplete": "new-password",
        }),
        strip=False,
    )

    agree = forms.BooleanField(
        error_messages={
            "required": "You must agree to continue."
        },
    )

    def clean_email(self):
        email = User.objects.normalize_email(
            self.cleaned_data["email"]
        ).lower()

        # Check both username and email to prevent duplicates.
        if User.objects.filter(
            Q(username__iexact=email) |
            Q(email__iexact=email)
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        # Custom password requirements.
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r"[^\w\s]", password):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        # Apply Django's configured password validators.
        try:
            password_validation.validate_password(password)
        except ValidationError as errors:
            raise forms.ValidationError(errors.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error(
                    "confirm_password",
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self):
        data = self.cleaned_data

        return User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
