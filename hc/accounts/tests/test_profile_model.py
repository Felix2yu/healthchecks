from __future__ import annotations

from datetime import datetime, timezone
from datetime import timedelta as td

import time_machine
from django.conf import settings
from django.core import mail
from django.test.utils import override_settings
from django.utils.timezone import now

from hc.api.models import Check, Flip
from hc.test import BaseTestCase

CURRENT_TIME = datetime(2020, 1, 13, 2, tzinfo=timezone.utc)

EMPTY_TABLE = """
+-----+-----+-----------+-----------+
| 状态  | 名称  | Nov. 2019 | Dec. 2019 |
+=====+=====+===========+===========+
| new | Foo |           |           |
+-----+-----+-----------+-----------+
""".strip()

NAG_TEXT = """您好，

这是由 Mychecks 发送的每小时 提醒。
当前有 1 个检查项宕机：


项目 "Alices Project"
+------+-----+--------------------+
| 状态   | 名称  | 上次 Ping            |
+======+=====+====================+
| DOWN | Foo | 1 week, 5 days ago |
+------+-----+--------------------+


--
此致，
Mychecks
"""


@override_settings(SITE_NAME="Mychecks")
@time_machine.travel(CURRENT_TIME)
class ProfileModelTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.check = Check(project=self.project, name="Foo")
        self.check.created = datetime(2019, 10, 1, tzinfo=timezone.utc)
        self.check.last_ping = datetime(2019, 12, 31, 23, tzinfo=timezone.utc)
        self.check.status = "down"
        self.check.save()

        self.flip = Flip(owner=self.check)
        self.flip.created = datetime(2019, 12, 31, 23, tzinfo=timezone.utc)
        self.flip.old_status = "new"
        self.flip.new_status = "down"
        self.flip.save()

    def test_send_report_sends_monthly_report(self) -> None:
        sent = self.profile.send_report()
        self.assertTrue(sent)

        # And an email should have been sent
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn("List-Unsubscribe", message.extra_headers)
        self.assertIn("List-Unsubscribe-Post", message.extra_headers)
        self.assertNotIn("X-Bounce-ID", message.extra_headers)

        self.assertEqual(message.subject, "Monthly 报告")

        # The summary line
        self.assertEmailContainsHtml(
            "December月，<strong>1 个检查项</strong>发生了 <strong>1 次宕机事件</strong>。"
        )
        self.assertEmailContainsText("December月，1 个检查项发生了 1 次宕机事件。")

        # Note, assertEmailContains tests if the fragment appears in
        # *both* text and HTML versions.
        self.assertEmailContains("Foo")

        # The report should cover Nov-Dec, and should not mention October or January
        self.assertEmailNotContains("Oct. 2020")
        self.assertEmailNotContains("Jan. 2020")

        # There were no downtimes in November 2019:
        self.assertEmailContainsHtml("Nov. 2019")
        self.assertEmailContains("一切正常！")

        # There was one hour downtime in December 2019 (the last hour before midnight)
        self.assertEmailContainsHtml("Dec. 2019")
        self.assertEmailContains("共计 1 小时 0 分钟")

        # Check UUIDs should not appear anywhere in the email
        self.assertEmailNotContains(str(self.check.code))

    def test_monthly_report_handles_no_downtimes(self) -> None:
        self.check.status = "up"
        self.check.save()
        self.flip.delete()

        self.profile.send_report()
        self.assertEmailContains("December月，没有检查项发生宕机。很棒！")

    def test_send_report_sends_weekly_report(self) -> None:
        self.profile.reports = "weekly"
        self.profile.save()

        self.profile.send_report()

        # The summary line
        self.assertEmailContainsHtml(
            "上周（1月6日 至 1月12日），<strong>1 个检查项</strong>发生了 <strong>1 次宕机事件</strong>。"
        )
        self.assertEmailContainsText(
            "上周（1月6日 至 1月12日），1 个检查项发生了 1 次宕机事件。"
        )

        email = mail.outbox[0]
        self.assertEqual(email.subject, "Weekly 报告")
        self.assertEmailContains("Dec 30 - Jan 5")
        self.assertEmailContains("Jan 6 - Jan 12")

    def test_send_report_sends_daily_report(self) -> None:
        self.profile.reports = "daily"
        self.profile.save()

        self.profile.send_report()

        # The summary line
        self.assertEmailContainsHtml(
            "昨天（1月12日），<strong>1 个检查项</strong>发生了 <strong>1 次宕机事件</strong>。"
        )
        self.assertEmailContainsText(
            "昨天（1月12日），1 个检查项发生了 1 次宕机事件。"
        )

        email = mail.outbox[0]
        self.assertEqual(email.subject, "Daily 报告")
        self.assertEmailContains("January 11")
        self.assertEmailContains("January 12")

    @override_settings(EMAIL_MAIL_FROM_TMPL="%s@bounces.example.org")
    def test_send_report_sets_custom_mail_from(self) -> None:
        self.profile.send_report()

        email = mail.outbox[0]
        self.assertTrue(email.from_email.startswith("r."))
        self.assertTrue(email.from_email.endswith("@bounces.example.org"))
        # The From header should contain the display address
        self.assertEqual(email.extra_headers["From"], settings.DEFAULT_FROM_EMAIL)
        # There should be no X-Bounce-ID header
        self.assertNotIn("X-Bounce-ID", email.extra_headers)

    def test_send_report_handles_recently_created_check(self) -> None:
        self.check.status = "new"
        self.check.created = datetime(2020, 1, 5, tzinfo=timezone.utc)
        self.check.save()

        self.flip.delete()

        self.profile.send_report()

        # The check did not exist in November-December 2019, so the email should not
        # contain strings "一切正常！" or "共计"
        self.assertEmailNotContains("一切正常！")
        self.assertEmailNotContains("共计")

        # Make sure the text version contains empty cells for months with no data
        self.assertEmailContainsText(EMPTY_TABLE)

    def test_send_report_does_not_escape_html_in_text_email(self) -> None:
        self.project.name = "Alice & Friends"
        self.project.save()

        self.check.name = "Foo & Bar"
        self.check.save()

        self.profile.send_report()

        self.assertEmailContainsText("Alice & Friends")
        self.assertEmailContainsText("Foo & Bar")

    def test_send_report_handles_positive_utc_offset(self) -> None:
        self.profile.reports = "weekly"
        self.profile.tz = "America/New_York"
        self.profile.save()

        self.profile.send_report()

        # UTC:      Monday, Jan 13, 2AM.
        # New York: Sunday, Jan 12, 9PM.
        # The report should not contain the Jan 6 - Jan 12 week, because
        # in New York it is the current week.
        self.assertEmailContains("Dec 23 - Dec 29")
        self.assertEmailContains("Dec 30 - Jan 5")
        self.assertEmailNotContains("Jan 6 - Jan 12")

        # Let's also verify the summary line
        self.assertEmailContains("上周（12月30日 至 1月5日）")

    def test_send_report_handles_negative_utc_offset(self) -> None:
        self.profile.reports = "weekly"
        self.profile.tz = "Asia/Tokyo"
        self.profile.save()

        self.profile.send_report()

        # UTC:   Monday, Jan 13, 2AM.
        # Tokyo: Monday, Jan 13, 11AM
        self.assertEmailNotContains("Dec 23 - Dec 29")
        self.assertEmailContains("Dec 30 - Jan 5")
        self.assertEmailContains("Jan 6 - Jan 12")

        # Let's also verify the summary line
        self.assertEmailContains("上周（1月6日 至 1月12日）")

    def test_send_report_noops_if_no_pings(self) -> None:
        self.check.delete()

        sent = self.profile.send_report()
        self.assertFalse(sent)

        self.assertEqual(len(mail.outbox), 0)

    def test_send_report_noops_if_no_recent_pings(self) -> None:
        self.check.last_ping = datetime(2019, 1, 1, tzinfo=timezone.utc)
        self.check.save()

        sent = self.profile.send_report()
        self.assertFalse(sent)

        self.assertEqual(len(mail.outbox), 0)

    def test_send_report_sends_nag(self) -> None:
        self.profile.nag_period = td(hours=1)
        self.profile.save()

        sent = self.profile.send_report(nag=True)
        self.assertTrue(sent)

        # And an email should have been sent
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]

        self.assertEqual(message.subject, "提醒：1 个检查项仍宕机")
        self.assertEqual(message.body, NAG_TEXT)
        self.assertEmailContains("Foo")

        # Check UUIDs should not appear anywhere in the email
        self.assertEmailNotContains(str(self.check.code))

    def test_send_nag_noops_if_none_down(self) -> None:
        self.check.last_ping = None
        self.check.status = "new"
        self.check.save()

        self.profile.nag_period = td(hours=1)
        self.profile.save()

        sent = self.profile.send_report(nag=True)
        self.assertFalse(sent)

        self.assertEqual(len(mail.outbox), 0)

    def test_send_nag_skips_up_checks(self) -> None:
        check2 = Check(project=self.project, last_ping=now())
        check2.name = "Foobar"
        check2.status = "up"
        check2.save()

        self.profile.send_report(nag=True)

        self.assertEmailContains("Foo")
        self.assertEmailNotContains("Foobar")

    def test_it_sets_next_nag_date(self) -> None:
        self.profile.nag_period = td(hours=1)
        self.profile.update_next_nag_date()

        self.assertTrue(self.profile.next_nag_date)

    def test_it_does_not_set_next_nag_date_if_no_nag_period(self) -> None:
        self.profile.update_next_nag_date()
        self.assertIsNone(self.profile.next_nag_date)

    def test_it_does_not_update_existing_next_nag_date(self) -> None:
        Check.objects.create(project=self.project, status="down")

        original_nag_date = now() - td(minutes=30)

        self.profile.next_nag_date = original_nag_date
        self.profile.nag_period = td(hours=1)
        self.profile.update_next_nag_date()

        self.assertEqual(self.profile.next_nag_date, original_nag_date)

    def test_it_clears_next_nag_date(self) -> None:
        self.check.last_ping = None
        self.check.status = "new"
        self.check.save()

        self.profile.next_nag_date = now()
        self.profile.update_next_nag_date()
        self.assertIsNone(self.profile.next_nag_date)
