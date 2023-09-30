from django.contrib import admin
from ticket.models import Ticket, TicketReply


class InlineTicketReplyAdmin(admin.TabularInline):
    model = TicketReply
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [InlineTicketReplyAdmin]
    list_display = ('title', 'created_by', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'created_by__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'created_by', 'created_at')
    search_fields = ('ticket__title', 'created_by__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
