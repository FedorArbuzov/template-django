from django.contrib import admin

from statsbot.models import Settings, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username')


admin.site.register(Settings)
admin.site.register(Profile)
