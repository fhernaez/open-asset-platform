from rest_framework.routers import DefaultRouter

from mqtt.views import (
    BrokerConnectionViewSet,
    MqttAgentViewSet,
    MqttBindingViewSet,
    MqttDiscoveryTemplateViewSet,
    MqttSubscriptionHealthViewSet,
)

router = DefaultRouter()
router.register("brokers", BrokerConnectionViewSet, basename="mqtt-broker")
router.register("agents", MqttAgentViewSet, basename="mqtt-agent")
router.register("bindings", MqttBindingViewSet, basename="mqtt-binding")
router.register("discovery", MqttDiscoveryTemplateViewSet, basename="mqtt-discovery")
router.register("health", MqttSubscriptionHealthViewSet, basename="mqtt-health")

urlpatterns = router.urls
