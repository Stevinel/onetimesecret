import datetime as dt

import pgcrypto
from django.db import models

LIFE_TIME = (
    ("1", "7 days"),
    ("2", "3 days"),
    ("3", "1 day"),
    ("4", "1 hour"),
    ("5", "30 minutes"),
    ("6", "5 minutes"),
)

DATE_NOW = dt.datetime.now()
TIME_OF_DEATH = {
    "1": (DATE_NOW + dt.timedelta(days=7)),
    "2": (DATE_NOW + dt.timedelta(days=3)),
    "3": (DATE_NOW + dt.timedelta(days=1)),
    "4": (DATE_NOW + dt.timedelta(hours=1)),
    "5": (DATE_NOW + dt.timedelta(minutes=30)),
    "6": (DATE_NOW + dt.timedelta(minutes=5)),
}


class Secret(models.Model):
    secret = pgcrypto.EncryptedCharField("Secret", max_length=100000)
    key_word = pgcrypto.EncryptedCharField("Pass phrase", max_length=100)
    is_viewed = models.CharField("Already viewed", max_length=100)
    slug = models.CharField("Slug", max_length=20, unique=True)
    lifetime = models.PositiveIntegerField(
        verbose_name="Lifetime",
        null=True,
        blank=True,
    )
    time_of_death = models.DateTimeField(
        "Secret end time", null=True, blank=True
    )
    created_date = models.DateTimeField("Created date", auto_now_add=True)

    class Meta:
        verbose_name = "Секрет"
        verbose_name_plural = "Секреты"

    def __str__(self):
        return self.secret
