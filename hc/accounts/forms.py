from __future__ import annotations

from datetime import timedelta as td
from typing import Any

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from pyotp.totp import TOTP

from hc.accounts.models import REPORT_CHOICES, Member
from hc.api.models import TokenBucket
from hc.front.validators import TimezoneValidator
from hc.lib.tz import all_timezones


class LowercaseEmailField(forms.EmailField):
    def clean(self, value: str) -> str:
        value = super().clean(value)
        return value.lower()


class SignupForm(forms.Form):
    # Call it "identity" instead of "email"
    # to avoid some of the dumber bots
    identity = LowercaseEmailField(
        error_messages={"required": "请输入您的邮箱地址。"}
    )
    tz = forms.CharField(required=False)

    def __init__(self, request: HttpRequest):
        self.request = request
        super().__init__(request.POST)

    def clean_identity(self) -> str:
        if not TokenBucket.authorize_auth_ip(self.request):
            raise forms.ValidationError("尝试次数过多，请稍后再试。")

        v = self.cleaned_data["identity"]
        assert isinstance(v, str)
        if len(v) > 254:
            raise forms.ValidationError("地址过长。")
        # When user signs up with an email address that already has an account
        # we send them the magic login link. Hence we must rate-limit attempts
        # to sign up with a specific email address the same as we would rate-limit
        # attempts to log in with that email address:
        if not TokenBucket.authorize_login_email(v):
            raise forms.ValidationError("尝试次数过多，请稍后再试。")

        return v

    def clean_tz(self) -> str | None:
        assert isinstance(self.cleaned_data["tz"], str)

        # Declare tz as "clean" only if we can find it in hc.lib.tz.all_timezones
        if self.cleaned_data["tz"] in all_timezones:
            return self.cleaned_data["tz"]

        # Otherwise, return None, and *don't* throw a validation exception:
        # If user's browser reports a timezone we don't recognize, we
        # should ignore the timezone but still save the rest of the form.
        return None


class EmailLoginForm(forms.Form):
    # Call it "identity" instead of "email"
    # to avoid some of the dumber bots
    identity = LowercaseEmailField()

    def __init__(self, request: HttpRequest | None = None):
        self.request = request
        super().__init__(request.POST if request else None)

    def clean_identity(self) -> str:
        v = self.cleaned_data["identity"]

        assert isinstance(v, str)
        if not TokenBucket.authorize_login_email(v):
            raise forms.ValidationError("尝试次数过多，请稍后再试。")

        assert self.request
        if not TokenBucket.authorize_auth_ip(self.request):
            raise forms.ValidationError("尝试次数过多，请稍后再试。")

        self.user: User | None
        try:
            self.user = User.objects.get(email=v)
        except User.DoesNotExist:
            self.user = None

        return v


class PasswordLoginForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField()

    def clean(self) -> dict[str, Any]:
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if username and password:
            if not TokenBucket.authorize_login_password(username):
                raise forms.ValidationError("尝试次数过多，请稍后再试。")

            self.user = authenticate(username=username, password=password)
            if self.user is None or not self.user.is_active:
                raise forms.ValidationError("邮箱或密码不正确。")

        return self.cleaned_data


class ReportSettingsForm(forms.Form):
    reports = forms.ChoiceField(choices=REPORT_CHOICES)
    nag_period = forms.IntegerField(min_value=0, max_value=86400)

    def clean_nag_period(self) -> td:
        seconds = self.cleaned_data["nag_period"]

        if seconds not in (0, 3600, 86400):
            raise forms.ValidationError(f"无效的重复提醒周期：{seconds}")

        return td(seconds=seconds)


class SetPasswordForm(forms.Form):
    password = forms.CharField(min_length=8)


class ChangeEmailForm(forms.Form):
    error_css_class = "has-error"
    email = LowercaseEmailField()

    def clean_email(self) -> str:
        v = self.cleaned_data["email"]
        assert isinstance(v, str)
        if User.objects.filter(email=v).exists():
            raise forms.ValidationError(f"{v} 已被注册")

        return v


class InviteTeamMemberForm(forms.Form):
    email = LowercaseEmailField(max_length=254)
    role = forms.ChoiceField(choices=Member.Role.choices)


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class ProjectNameForm(forms.Form):
    name = forms.CharField(max_length=60)


class TransferForm(forms.Form):
    email = LowercaseEmailField()


class AddWebAuthnForm(forms.Form):
    name = forms.CharField(max_length=100)
    response = forms.CharField()


class WebAuthnForm(forms.Form):
    response = forms.CharField()


class TotpForm(forms.Form):
    error_css_class = "has-error"
    code = forms.RegexField(regex=r"^\d{6}$")

    def __init__(self, totp: TOTP, post: Any = None):
        self.totp = totp
        super().__init__(post)

    def clean_code(self) -> str:
        assert isinstance(self.cleaned_data["code"], str)
        if not self.totp.verify(self.cleaned_data["code"], valid_window=1):
            raise forms.ValidationError("您输入的验证码不正确。")

        return self.cleaned_data["code"]


class TzForm(forms.Form):
    tz = forms.CharField(max_length=36, validators=[TimezoneValidator()])


class LeaveForm(forms.Form):
    code = forms.UUIDField()
