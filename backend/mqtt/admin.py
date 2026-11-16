from django.contrib import admin

from mqtt.models import (
    BrokerConnection,
    MqttAgent,
    MqttBinding,
    MqttDiscoveryTemplate,
    MqttSubscriptionHealth,
)


@admin.register(BrokerConnection)
class BrokerConnectionAdmin(admin.ModelAdmin):
    list_display = ["name", "host", "port", "tls", "tenant"]


@admin.register(MqttAgent)
class MqttAgentAdmin(admin.ModelAdmin):
    list_display = ["name", "broker", "connection_status", "tenant"]


@admin.register(MqttBinding)
class MqttBindingAdmin(admin.ModelAdmin):
    list_display = ["agent", "attribute", "subscribe_topic", "json_path"]


@admin.register(MqttDiscoveryTemplate)
class MqttDiscoveryTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "topic_pattern", "approval_required"]


@admin.register(MqttSubscriptionHealth)
class MqttSubscriptionHealthAdmin(admin.ModelAdmin):
    list_display = ["agent", "connectivity", "received", "published", "backpressure"]
