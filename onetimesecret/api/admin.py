from django.contrib import admin

from .models import Secret


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "secret",
        "key_word",
        "is_viewed",
        "slug",
        "lifetime",
        "created_date",
        "time_of_death",
    )
    search_fields = ("secret",)
    list_filter = ("created_date", "time_of_death")
    empty_value_display = "-пусто-"
