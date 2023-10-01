from django.contrib import admin
from raad import models
from raad.forms import CompanyAdminForm


@admin.register(models.AllowedIp)
class AllowedIpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')


class InlineDeviceAdmin(admin.TabularInline):
    model = models.Device
    extra = 1


class InlineMessengerAdmin(admin.TabularInline):
    model = models.MessengerAdmin
    extra = 1


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm
    inlines = [InlineDeviceAdmin, InlineMessengerAdmin]

    list_display = ('id', 'name', 'license_key', 'expiration_date')
    list_filter = ('expiration_date',)
    search_fields = ('name',)


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_activated', 'company')
    list_filter = ('company',)
    search_fields = ('name', 'license_key')


@admin.register(models.MessengerAdmin)
class MessengerAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'messenger', 'admin_messenger_id', 'company')
    list_filter = ('messenger', 'company')
    search_fields = ('admin_messenger_id',)
