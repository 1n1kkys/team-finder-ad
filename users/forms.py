import uuid

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.utils import normalize_phone

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.phone = f"8{uuid.uuid4().int % 10**10:010d}"
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Неверный email или пароль"
                )
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        widgets = {
            "avatar": forms.FileInput(),
            "about": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_phone(self):
        return normalize_phone(self.cleaned_data["phone"])

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Текущий пароль",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Новый пароль",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтвердите новый пароль",
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data


class AdminUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("email", "name", "surname", "phone")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Пароль",
        help_text="Пароль хранится в виде хеша и здесь не редактируется.",
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "name",
            "surname",
            "avatar",
            "phone",
            "github_url",
            "about",
            "favorites",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
