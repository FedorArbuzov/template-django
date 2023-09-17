from django.contrib import admin

from bot.models import Settings, Profile, Order, Tariff


admin.site.register(Settings)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'is_premium', 'premium_bought_to')


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'number')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'profile_username', 'subscribe_type', 'paid')

    def profile_username(self, obj):
        return obj.profile.username