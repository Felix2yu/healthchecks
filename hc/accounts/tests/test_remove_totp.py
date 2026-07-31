from __future__ import annotations

from hc.accounts.models import Credential
from hc.test import BaseTestCase


class RemoveCredentialTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.profile.totp = "0" * 32
        self.profile.save()

        self.url = "/accounts/two_factor/totp/remove/"

    def test_it_requires_sudo_mode(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        r = self.client.get(self.url)
        self.assertContains(r, "我们已向您的邮箱地址发送了一个确认码。")

    def test_it_shows_form(self) -> None:
        self.client.login(username="alice@example.org", password="password")
        self.set_sudo_flag()

        r = self.client.get(self.url)
        self.assertContains(r, "禁用身份验证器应用")
        self.assertContains(r, "双重身份验证将不再生效。")

    def test_it_skips_warning_when_other_2fa_methods_exist(self) -> None:
        self.c = Credential.objects.create(user=self.alice, name="Alices Key")
        self.client.login(username="alice@example.org", password="password")
        self.set_sudo_flag()

        r = self.client.get(self.url)
        self.assertNotContains(r, "双重身份验证将不再生效。")

    def test_it_removes_totp(self) -> None:
        self.client.login(username="alice@example.org", password="password")
        self.set_sudo_flag()

        r = self.client.post(self.url, {"disable_totp": "1"}, follow=True)
        self.assertRedirects(r, "/accounts/profile/")
        self.assertContains(r, "已禁用身份验证器应用。")

        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.totp)
        self.assertIsNone(self.profile.totp_created)
