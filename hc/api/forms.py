from __future__ import annotations

from datetime import datetime, timezone

from django import forms
from django.core.exceptions import ValidationError


class TimestampField(forms.Field):
    def to_python(self, value: str | None) -> datetime | None:
        if value is None:
            return None

        try:
            value_int = int(value)
        except ValueError:
            raise ValidationError(message="必须为整数")

        # 10000000000 is year 2286 (a sanity check)
        if value_int < 0 or value_int > 10000000000:
            raise ValidationError(message="超出范围")

        return datetime.fromtimestamp(value_int, timezone.utc)


class FlipsFiltersForm(forms.Form):
    start = TimestampField(required=False)
    end = TimestampField(required=False)
    seconds = forms.IntegerField(required=False, min_value=0, max_value=31536000)
