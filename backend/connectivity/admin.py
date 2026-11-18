from django.contrib import admin

from connectivity.models import Gateway, GatewayBinding


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ["asset", "protocol", "connection_status", "tenant"]


@admin.register(GatewayBinding)
class GatewayBindingAdmin(admin.ModelAdmin):
    list_display = ["gateway", "attribute", "address", "mapping"]
