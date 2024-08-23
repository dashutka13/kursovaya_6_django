from django.contrib import admin

from emailing.models import Emailing, Client, EmailingLog, Messages


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'description')
    search_fields = ('email',)


@admin.register(Emailing)
class EmailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'send_periodicity', 'emailing_status', 'display_mailing_clients')
    search_fields = ('send_periodicity', 'emailing_status', 'emailing_clients')

    def display_mailing_clients(self, obj):
        return ', '.join([client.email for client in obj.emailing_clients.all()])

    display_mailing_clients.short_description = 'Emailing Clients'


@admin.register(EmailingLog)
class EmailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'log_status', 'response',)
    search_fields = ('log_status',)


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('topic', )
    list_filter = ('topic',)
    search_fields = ('topic',)
