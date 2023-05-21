from django.contrib import admin

from bot.models import Settings, Proile, Messages, Posts

from bot.send_messages import send_message_to_group

admin.site.register(Settings)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'message_count', 'is_premium')


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_send_by_user', 'created_at')


admin.site.register(Messages, MessagesAdmin)
admin.site.register(Proile, ProfileAdmin)



@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('content', 'group')

    def save_model(self, request, obj, form, change):
        print('send_posts')
        users = send_message_to_group(obj.content, obj.group)
        obj.target_users = users
        obj.is_send = True
        super().save_model(request, obj, form, change)