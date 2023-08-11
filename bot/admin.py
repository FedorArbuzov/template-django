from django.contrib import admin

from bot.models import Settings, Profile, Order, Tariff


admin.site.register(Settings)

admin.site.register(Profile)


@admin.register(Tariff)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'number')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'subscribe_type', 'paid')