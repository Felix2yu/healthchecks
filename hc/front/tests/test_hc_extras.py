from __future__ import annotations

from datetime import timedelta as td
from unittest import TestCase
from urllib.parse import urlparse

from django.test.utils import override_settings

from hc.front.templatetags.hc_extras import (
    absolute_site_logo_url,
    hc_duration,
    mask_key,
    mask_ro_key,
    mask_rw_key,
    site_hostname,
)


class HcExtrasTestCase(TestCase):
    def test_hc_duration_works(self) -> None:
        samples = [
            (60, "1 分钟"),
            (120, "2 分钟"),
            (3600, "1 小时"),
            (3660, "1 小时 1 分钟"),
            (86400, "1 天"),
            (604800, "1 周"),
            (2419200, "4 周"),
            (2592000, "30 天"),
            (3801600, "44 天"),
        ]

        for seconds, expected_result in samples:
            result = hc_duration(td(seconds=seconds))
            self.assertEqual(result, expected_result)


class AbsoluteSiteLogoUrlTestCase(TestCase):
    def _test(
        self, site_root: str, site_logo_url: str | None, expected_result: str
    ) -> None:
        subpath = urlparse(site_root).path
        with override_settings(
            SITE_ROOT=site_root,
            SITE_LOGO_URL=site_logo_url,
            STATIC_URL=f"{subpath}/static/",
        ):
            self.assertEqual(absolute_site_logo_url(), expected_result)

    def test_it_handles_default(self) -> None:
        self._test(
            site_root="http://example.org",
            site_logo_url=None,
            expected_result="http://example.org/static/img/logo.png",
        )

    def test_it_handles_default_with_subpath(self) -> None:
        self._test(
            site_root="http://example.org/subpath",
            site_logo_url=None,
            expected_result="http://example.org/subpath/static/img/logo.png",
        )

    def test_it_handles_external_url(self) -> None:
        self._test(
            site_root="http://example.org",
            site_logo_url="http://example.com/foo.png",
            expected_result="http://example.com/foo.png",
        )

    def test_it_handles_leading_slash(self) -> None:
        self._test(
            site_root="http://example.org",
            site_logo_url="/foo/bar.png",
            expected_result="http://example.org/foo/bar.png",
        )

    def test_it_handles_leading_slash_with_subpath(self) -> None:
        self._test(
            site_root="http://example.org/subpath",
            site_logo_url="/foo/bar.png",
            expected_result="http://example.org/foo/bar.png",
        )


class SiteHostnameTestCase(TestCase):
    @override_settings(SITE_ROOT="http://example.org")
    def test_it_works(self) -> None:
        self.assertEqual(site_hostname(), "example.org")

    @override_settings(SITE_ROOT="http://example.org/foo")
    def test_it_handles_subpath(self) -> None:
        self.assertEqual(site_hostname(), "example.org")


class MaskKeyTestCase(TestCase):
    def test_it_works(self) -> None:
        self.assertEqual(mask_key("X" * 32), "XXXX" + "*" * 28)

    def test_it_handles_hashed_key(self) -> None:
        key = f"ABCDEFGH.{'0' * 64}"
        self.assertEqual(mask_rw_key(key), "hcw_ABCD" + "*" * 24)
        self.assertEqual(mask_ro_key(key), "hcr_ABCD" + "*" * 24)
