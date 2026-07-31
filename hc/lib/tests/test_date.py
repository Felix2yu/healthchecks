from __future__ import annotations

from datetime import date, datetime, timezone
from datetime import timedelta as td
from unittest import TestCase

import time_machine

from hc.lib.date import (
    day_boundaries,
    format_approx_duration,
    format_duration_for_sentence,
    format_hms,
    month_boundaries,
    seconds_in_month,
    week_boundaries,
)

CURRENT_TIME = datetime(2020, 1, 15, tzinfo=timezone.utc)


class DateFormattingTestCase(TestCase):
    def test_sub_second_works(self) -> None:
        s = format_hms(td(seconds=0.12))
        self.assertEqual(s, "0.12 秒")

    def test_mins_secs_work(self) -> None:
        s = format_hms(td(seconds=0))
        self.assertEqual(s, "0 秒")

        s = format_hms(td(seconds=1))
        self.assertEqual(s, "1 秒")

        s = format_hms(td(seconds=61))
        self.assertEqual(s, "1 分钟 1 秒")

        s = format_hms(td(seconds=62))
        self.assertEqual(s, "1 分钟 2 秒")

    def test_hours_work(self) -> None:
        s = format_hms(td(seconds=62 + 60 * 60))
        self.assertEqual(s, "1 小时 1 分钟 2 秒")

        s = format_hms(td(seconds=60 * 60))
        self.assertEqual(s, "1 小时 0 分钟 0 秒")


class ApproxFormattingTestCase(TestCase):
    def test_days_work(self) -> None:
        s = format_approx_duration(td(days=3, hours=6, minutes=12, seconds=24))
        self.assertEqual(s, "3 天 6 小时")

    def test_one_day_works(self) -> None:
        s = format_approx_duration(td(days=1, hours=6, minutes=12, seconds=24))
        self.assertEqual(s, "1 天 6 小时")

    def test_hours_work(self) -> None:
        s = format_approx_duration(td(hours=6, minutes=12, seconds=24))
        self.assertEqual(s, "6 小时 12 分钟")

    def test_minutes_work(self) -> None:
        s = format_approx_duration(td(minutes=12, seconds=24))
        self.assertEqual(s, "12 分钟 24 秒")


class ForSentenceFormattingTestCase(TestCase):
    def test_it_works(self) -> None:
        samples = [
            (td(days=3, hours=6, minutes=12, seconds=24), "3 天, 6 小时"),
            (td(days=1, hours=6, minutes=12, seconds=24), "1 天, 6 小时"),
            (td(days=3, hours=1, minutes=12, seconds=24), "3 天, 1 小时"),
            (td(hours=6, minutes=12, seconds=24), "6 小时, 12 分钟"),
            (td(hours=1, minutes=12, seconds=24), "1 小时, 12 分钟"),
            (td(hours=6, minutes=1, seconds=24), "6 小时, 1 分钟"),
            (td(minutes=12, seconds=24), "12 分钟, 24 秒"),
            (td(minutes=1, seconds=24), "1 分钟, 24 秒"),
            (td(minutes=12, seconds=1), "12 分钟, 1 秒"),
            (td(seconds=12), "12 秒"),
            (td(seconds=1), "1 秒"),
            (td(milliseconds=500), "0 秒"),
        ]

        for duration, expected in samples:
            self.assertEqual(format_duration_for_sentence(duration), expected)


@time_machine.travel(CURRENT_TIME)
class MonthBoundaryTestCase(TestCase):
    def test_utc_works(self) -> None:
        result = month_boundaries(3, "UTC")
        self.assertEqual(result[0].isoformat(), "2020-01-01T00:00:00+00:00")
        self.assertEqual(result[1].isoformat(), "2019-12-01T00:00:00+00:00")
        self.assertEqual(result[2].isoformat(), "2019-11-01T00:00:00+00:00")

    def test_non_utc_works(self) -> None:
        result = month_boundaries(3, "Europe/Riga")
        self.assertEqual(result[0].isoformat(), "2020-01-01T00:00:00+02:00")
        self.assertEqual(result[1].isoformat(), "2019-12-01T00:00:00+02:00")
        self.assertEqual(result[2].isoformat(), "2019-11-01T00:00:00+02:00")


@time_machine.travel(CURRENT_TIME)
class WeekBoundaryTestCase(TestCase):
    def test_utc_works(self) -> None:
        result = week_boundaries(3, "UTC")
        self.assertEqual(result[0].isoformat(), "2020-01-13T00:00:00+00:00")
        self.assertEqual(result[1].isoformat(), "2020-01-06T00:00:00+00:00")
        self.assertEqual(result[2].isoformat(), "2019-12-30T00:00:00+00:00")

    def test_non_utc_works(self) -> None:
        result = week_boundaries(3, "Europe/Riga")
        self.assertEqual(result[0].isoformat(), "2020-01-13T00:00:00+02:00")
        self.assertEqual(result[1].isoformat(), "2020-01-06T00:00:00+02:00")
        self.assertEqual(result[2].isoformat(), "2019-12-30T00:00:00+02:00")


@time_machine.travel(CURRENT_TIME)
class DayBoundaryTestCase(TestCase):
    def test_utc_works(self) -> None:
        result = day_boundaries(3, "UTC")
        self.assertEqual(result[0].isoformat(), "2020-01-15T00:00:00+00:00")
        self.assertEqual(result[1].isoformat(), "2020-01-14T00:00:00+00:00")
        self.assertEqual(result[2].isoformat(), "2020-01-13T00:00:00+00:00")

    def test_non_utc_works(self) -> None:
        result = day_boundaries(3, "Europe/Riga")
        self.assertEqual(result[0].isoformat(), "2020-01-15T00:00:00+02:00")
        self.assertEqual(result[1].isoformat(), "2020-01-14T00:00:00+02:00")
        self.assertEqual(result[2].isoformat(), "2020-01-13T00:00:00+02:00")


class SecondsInMonthTestCase(TestCase):
    def test_utc_works(self) -> None:
        result = seconds_in_month(date(2023, 10, 1), "UTC")
        self.assertEqual(result, 31 * 24 * 60 * 60)

    def test_it_handles_dst_extra_hour(self) -> None:
        result = seconds_in_month(date(2023, 10, 1), "Europe/Riga")
        self.assertEqual(result, 31 * 24 * 60 * 60 + 60 * 60)

    def test_it_handles_dst_skipped_hour(self) -> None:
        result = seconds_in_month(date(2024, 3, 1), "Europe/Riga")
        self.assertEqual(result, 31 * 24 * 60 * 60 - 60 * 60)
