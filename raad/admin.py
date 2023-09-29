from django.contrib import admin
from raad import models


@admin.register(models.AllowedIp)
class AllowedIpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')


# @admin.register(models.Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user')


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'expiration_date')
    list_filter = ('expiration_date',)
    search_fields = ('name',)


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'license_key', 'company')
    list_filter = ('company',)
    search_fields = ('name', 'license_key')


@admin.register(models.MessengerAdmin)
class MessengerAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'messenger', 'admin_messenger_id', 'company')
    list_filter = ('messenger', 'company')
    search_fields = ('admin_messenger_id',)
