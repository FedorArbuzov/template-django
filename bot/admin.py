from django.contrib import admin

from bot.models import Settings, Proile, Messages

admin.site.register(Settings)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'message_count', 'is_premium')


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_send_by_user', 'created_at')


admin.site.register(Messages, MessagesAdmin)
admin.site.register(Proile, ProfileAdmin)