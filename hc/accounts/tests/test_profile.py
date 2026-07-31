from __future__ import annotations

from django.test.utils import override_settings

from hc.accounts.models import Credential
from hc.test import BaseTestCase


class ProfileTestCase(BaseTestCase):
    def test_it_shows_profile_page(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "邮箱与密码")
        self.assertContains(r, "修改密码")
        self.assertContains(r, "设置身份验证器应用")

    def test_leaving_works(self) -> None:
        self.client.login(username="bob@example.org", password="password")

        form = {"code": str(self.project.code), "leave_project": "1"}
        r = self.client.post("/accounts/profile/", form)
        self.assertContains(r, "已离开项目 <strong>Alices Project</strong>。")
        self.assertNotContains(r, "Member")

        self.bobs_profile.refresh_from_db()
        self.assertFalse(self.bob.memberships.exists())

    def test_leaving_checks_membership(self) -> None:
        self.client.login(username="charlie@example.org", password="password")

        form = {"code": str(self.project.code), "leave_project": "1"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 400)

    def test_leaving_handles_invalid_uuid(self) -> None:
        self.client.login(username="bob@example.org", password="password")

        form = {"code": "surprise", "leave_project": "1"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 400)

    def test_it_shows_project_membership(self) -> None:
        self.client.login(username="bob@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "Alices Project")
        self.assertContains(r, "Member")

    def test_it_shows_readonly_project_membership(self) -> None:
        self.bobs_membership.role = "r"
        self.bobs_membership.save()

        self.client.login(username="bob@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "Alices Project")
        self.assertContains(r, "Read-only")

    def test_it_handles_no_projects(self) -> None:
        self.project.delete()

        self.client.login(username="alice@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "您还没有任何项目。创建一个！")

    @override_settings(RP_ID=None)
    def test_it_hides_security_keys_bits_if_rp_id_not_set(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "双重身份验证")
        self.assertNotContains(r, "安全密钥")
        self.assertNotContains(r, "添加安全密钥")

    @override_settings(RP_ID="testserver")
    def test_it_handles_no_credentials(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "双重身份验证")
        self.assertContains(r, "您的账户未配置任何双重身份验证方法。")

    @override_settings(RP_ID="testserver")
    def test_it_shows_security_key(self) -> None:
        Credential.objects.create(user=self.alice, name="Alices Key")

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "Alices Key")

        # It should show a warning about Alices Key being the only second factor
        s = """密钥"Alices Key"目前是您唯一的第二重身份验证。"""
        self.assertContains(r, s)

    def test_it_handles_unusable_password(self) -> None:
        self.alice.set_unusable_password()
        self.alice.save()

        # Authenticate using the ProfileBackend and a token:
        token = self.profile.prepare_token()
        self.client.login(username="alice", token=token)

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "设置密码")
        self.assertNotContains(r, "修改密码")

    @override_settings(RP_ID="testserver")
    def test_it_shows_totp(self) -> None:
        self.profile.totp = "0" * 32
        self.profile.totp_created = "2020-01-01T00:00:00+00:00"
        self.profile.save()

        self.client.login(username="alice@example.org", password="password")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "已启用")
        self.assertContains(r, "配置于 Jan 1, 2020")
        self.assertNotContains(r, "设置身份验证器应用")

        # It should show a warning about TOTP being the only second factor
        s = "身份验证器应用目前是您唯一的第二重身份验证。"
        self.assertContains(r, s)
        self.assertContains(r, "或注册一个安全密钥作为备份的第二重身份验证")

    def test_it_shows_no_warning_if_multiple_keys_are_registered(self) -> None:
        Credential.objects.create(user=self.alice, name="Alices Key")
        Credential.objects.create(user=self.alice, name="Alices Other Key")

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/accounts/profile/")

        self.assertNotContains(r, "目前是您唯一的第二重身份验证。")

    def test_it_shows_no_warning_if_key_and_totp_is_registered(self) -> None:
        Credential.objects.create(user=self.alice, name="Alices Key")
        self.profile.totp = "0" * 32
        self.profile.totp_created = "2020-01-01T00:00:00+00:00"
        self.profile.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/accounts/profile/")

        self.assertNotContains(r, "目前是您唯一的第二重身份验证。")

    @override_settings(RP_ID=None)
    def test_it_does_not_mention_security_key_if_rp_id_is_not_set(self) -> None:
        self.profile.totp = "0" * 32
        self.profile.totp_created = "2020-01-01T00:00:00+00:00"
        self.profile.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/accounts/profile/")
        self.assertNotContains(r, "或注册一个安全密钥作为备份的第二重身份验证")

    def test_it_saves_tz(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        r = self.client.post("/accounts/profile/", {"tz": "Europe/Riga"})

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.tz, "Europe/Riga")
        self.assertContains(r, "时区已更新！")

    def test_it_ignores_bad_tz(self) -> None:
        self.client.login(username="alice@example.org", password="password")

        self.client.post("/accounts/profile/", {"tz": "Foo/Bar"})

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.tz, "UTC")
