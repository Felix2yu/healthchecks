from __future__ import annotations

from django.core import mail
from django.core.signing import TimestampSigner

from hc.accounts.models import Credential
from hc.api.models import TokenBucket
from hc.test import BaseTestCase


class SudoModeTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.c = Credential.objects.create(user=self.alice, name="Alices Key")
        self.url = "/accounts/set_password/"

    def test_it_sends_code(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        r = self.client.get(self.url)
        self.assertContains(r, "我们已向您的邮箱地址发送了一个确认码。")

        # A code should have been sent
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.to[0], "alice@example.org")
        self.assertIn("确认码", email.subject)

    def test_it_accepts_code(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["sudo_code"] = TimestampSigner().sign("123456")
        session.save()

        r = self.client.post(self.url, {"sudo_code": "123456"})
        self.assertRedirects(r, self.url)

        # sudo mode should now be active
        self.assertIn("sudo", self.client.session)

    def test_it_rejects_incorrect_code(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["sudo_code"] = TimestampSigner().sign("123456")
        session.save()

        r = self.client.post(self.url, {"sudo_code": "000000"})
        self.assertContains(r, "验证码无效")

        # sudo mode should *not* be active
        self.assertNotIn("sudo", self.client.session)

    def test_it_passes_through_if_sudo_mode_is_active(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["sudo"] = TimestampSigner().sign("active")
        session.save()

        r = self.client.get(self.url)
        self.assertContains(r, "请为您的 Mychecks 账户选择一个密码。")

    def test_it_uses_rate_limiting(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        obj = TokenBucket(value=f"sudo-{self.alice.id}")
        obj.tokens = 0
        obj.save()

        r = self.client.get(self.url)
        self.assertContains(r, "请求过多")
