from __future__ import annotations

import json
from datetime import timedelta as td
from unittest.mock import Mock, patch

from django.utils.timezone import now

from hc.api.models import Channel, Check, Flip, Notification, Ping, TokenBucket
from hc.test import BaseTestCase


class NotifyTelegramTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.check = Check(project=self.project)
        self.check.name = "DB Backup"
        self.check.tags = "foo bar baz"
        # Transport classes should use flip.new_status,
        # so the status "paused" should not appear anywhere
        self.check.status = "paused"
        self.check.last_ping = now()
        self.check.n_pings = 1
        self.check.save()

        self.ping = Ping(owner=self.check)
        self.ping.created = now() - td(minutes=10)
        self.ping.n = 112233
        self.ping.save()

        self.channel = Channel(project=self.project)
        self.channel.kind = "telegram"
        self.channel.value = json.dumps({"id": 123})
        self.channel.save()
        self.channel.checks.add(self.check)

        self.flip = Flip(owner=self.check)
        self.flip.created = now()
        self.flip.old_status = "new"
        self.flip.new_status = "down"
        self.flip.reason = "timeout"

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_works(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.channel.notify(self.flip)
        assert Notification.objects.count() == 1

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["chat_id"], 123)
        self.assertIsNone(payload["message_thread_id"])
        self.assertIn("检查项", payload["text"])
        self.assertIn(">DB Backup</a>", payload["text"])
        self.assertIn(self.check.cloaked_url(), payload["text"])
        self.assertIn("grace time passed", payload["text"])

        self.assertIn("<b>项目：</b> Alices Project\n", payload["text"])
        self.assertIn("<b>标签：</b> foo, bar, baz\n", payload["text"])
        self.assertIn("<b>周期：</b> 1 天\n", payload["text"])
        self.assertIn("<b>总 Ping 数：</b> 112233\n", payload["text"])
        self.assertIn("<b>上次 Ping：</b> Success，10 minutes ago", payload["text"])

        # Only one check in the project, so there should be no note about
        # other checks:
        self.assertNotIn("所有其他检查项都已恢复。", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_handles_reason_failure(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.flip.reason = "fail"
        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("received a failure signal", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_reports_down_duration(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.flip.save()

        up_flip = Flip(owner=self.check)
        up_flip.created = self.flip.created + td(minutes=90)
        up_flip.old_status = "down"
        up_flip.new_status = "up"
        self.channel.notify(up_flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("宕机持续了 1 小时, 30 分钟。", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_shows_exitstatus(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.ping.kind = "fail"
        self.ping.exitstatus = 123
        self.ping.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn(
            "<b>上次 Ping：</b> Exit status 123，10 minutes ago", payload["text"]
        )

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_sends_to_thread(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.channel.value = json.dumps({"id": 123, "thread_id": 456})
        self.channel.save()
        self.channel.notify(self.flip)
        assert Notification.objects.count() == 1

        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["chat_id"], 123)
        self.assertEqual(payload["message_thread_id"], 456)

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_shows_cron_schedule(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.check.kind = "cron"
        self.check.schedule = "* * * * MON-FRI"
        self.check.tz = "Europe/Riga"
        self.check.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn(
            "<b>计划：</b> <code>* * * * MON-FRI</code>\n", payload["text"]
        )
        self.assertIn("<b>时区：</b> Europe/Riga\n", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_shows_oncalendar_schedule(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.check.kind = "oncalendar"
        self.check.schedule = "Mon 2-29"
        self.check.tz = "Europe/Riga"
        self.check.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("<b>计划：</b> <code>Mon 2-29</code>\n", payload["text"])
        self.assertIn("<b>时区：</b> Europe/Riga\n", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_returns_error(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 400
        mock_post.return_value.content = b'{"description": "Hi"}'

        self.channel.notify(self.flip)
        n = Notification.objects.get()
        self.assertEqual(n.error, 'Received status code 400 with a message: "Hi"')

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_handles_non_json_error(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 400
        mock_post.return_value.json = Mock(side_effect=ValueError)

        self.channel.notify(self.flip)
        n = Notification.objects.get()
        self.assertEqual(n.error, "Received status code 400")

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_handles_group_supergroup_migration(self, mock_post: Mock) -> None:
        error_response = Mock(status_code=400)
        error_response.content = b"""{
            "description": "Hello",
            "parameters": {"migrate_to_chat_id": -234}
        }"""

        mock_post.side_effect = [error_response, Mock(status_code=200)]

        self.channel.notify(self.flip)
        self.assertEqual(mock_post.call_count, 2)

        # The chat id should have been updated
        self.channel.refresh_from_db()
        self.assertEqual(self.channel.telegram.id, -234)

        # There should be no logged error
        n = Notification.objects.get()
        self.assertEqual(n.error, "")

    def test_it_obeys_rate_limit(self) -> None:
        TokenBucket.objects.create(value="tg-123", tokens=0)

        self.channel.notify(self.flip)
        n = Notification.objects.get()
        self.assertEqual(n.error, "Rate limit exceeded")

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_shows_all_other_checks_up_note(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        other = Check(project=self.project)
        other.name = "Foobar"
        other.status = "up"
        other.last_ping = now() - td(minutes=61)
        other.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("所有其他检查项都已恢复。", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_lists_other_down_checks(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        other = Check(project=self.project)
        other.name = "Foobar"
        other.status = "down"
        other.last_ping = now() - td(minutes=61)
        other.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("以下检查项也处于宕机状态", payload["text"])
        self.assertIn("Foobar", payload["text"])
        self.assertIn("（上次 Ping：an hour ago）", payload["text"])
        self.assertIn(other.cloaked_url(), payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_handles_other_checks_with_no_last_ping(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        Check.objects.create(project=self.project, status="down")

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("（上次 Ping：从未）", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_does_not_show_more_than_10_other_checks(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        for i in range(11):
            other = Check(project=self.project)
            other.name = f"Foobar #{i}"
            other.status = "down"
            other.last_ping = now() - td(minutes=61)
            other.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertNotIn("Foobar", payload["text"])
        self.assertIn("其他 11 个检查项也处于宕机状态。", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_disables_channel_on_403(self, mock_post: Mock) -> None:
        messages = [
            "Forbidden: the group chat was deleted",
            "Forbidden: bot was blocked by the user",
            "Forbidden: user is deactivated",
            "Forbidden: bot was kicked from the group chat",
            "Forbidden: bot was kicked from the supergroup chat",
        ]

        for m in messages:
            mock_post.return_value.status_code = 403
            mock_post.return_value.content = json.dumps({"description": m}).encode()

            # Reset the disabled flag before each sub-test:
            self.channel.disabled = False
            self.channel.save()

            self.channel.notify(self.flip)
            self.channel.refresh_from_db()
            self.assertTrue(self.channel.disabled, f"Not disabled for {m}")

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_does_not_disable_on_unknown_403(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 403
        mock_post.return_value.content = json.dumps({"description": "oops"}).encode()

        self.channel.notify(self.flip)
        self.channel.refresh_from_db()
        self.assertFalse(self.channel.disabled)

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_disables_channel_on_chat_not_found(self, mock_post: Mock) -> None:
        m = "Bad Request: chat not found"
        mock_post.return_value.status_code = 400
        mock_post.return_value.content = json.dumps({"description": m}).encode()

        # Reset the disabled flag before each sub-test:
        self.channel.disabled = False
        self.channel.save()

        self.channel.notify(self.flip)
        self.channel.refresh_from_db()
        self.assertTrue(self.channel.disabled, f"Not disabled for {m}")

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_does_not_disable_on_unknown_400(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 400
        mock_post.return_value.content = json.dumps({"description": "oops"}).encode()

        self.channel.notify(self.flip)
        self.channel.refresh_from_db()
        self.assertFalse(self.channel.disabled)

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_shows_last_ping_body(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.ping.body_raw = b"Hello World"
        self.ping.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("<b>上次 Ping 正文：</b>\n", payload["text"])
        self.assertIn("Hello World", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_shows_truncated_last_ping_body(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.ping.body_raw = b"Hello World" * 100
        self.ping.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("[已截断]", payload["text"])

    @patch("hc.api.transports.curl.request", autospec=True)
    def test_it_escapes_html(self, mock_post: Mock) -> None:
        mock_post.return_value.status_code = 200

        self.ping.body_raw = b"<b>bold</b>\nfoo & bar"
        self.ping.save()

        self.channel.notify(self.flip)

        payload = mock_post.call_args.kwargs["json"]
        self.assertIn("&lt;b&gt;bold&lt;/b&gt;\n", payload["text"])
        self.assertIn("foo &amp; bar", payload["text"])
