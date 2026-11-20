from __future__ import annotations

from rest_framework import serializers

from spatial.models import Scene, SceneLayer, ScenePlacement


class SceneLayerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SceneLayer
        fields = ["id", "scene", "key", "name", "image", "image_url", "opacity", "order"]
        extra_kwargs = {"scene": {"required": False}}

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return None
        url = obj.image.url
        if request:
            return request.build_absolute_uri(url)
        return url


class ScenePlacementSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source="asset.name", read_only=True)

    class Meta:
        model = ScenePlacement
        fields = ["id", "scene", "layer", "asset", "asset_name", "x", "y", "z", "symbol"]
        extra_kwargs = {"scene": {"required": False}}


class SceneSerializer(serializers.ModelSerializer):
    layers = SceneLayerSerializer(many=True, read_only=True)
    placements = ScenePlacementSerializer(many=True, read_only=True)

    class Meta:
        model = Scene
        fields = ["id", "tenant", "project", "name", "description", "layers", "placements"]
        extra_kwargs = {
            "tenant": {"required": False},
            "project": {"required": False, "allow_null": True},
        }
