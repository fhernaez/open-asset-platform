from django.contrib import admin

from assets.models import Asset, AssetAttribute, AssetRelationship, AssetType, Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["symbol", "name", "quantity"]


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "tenant"]


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["name", "external_ref", "asset_type", "tenant", "project", "status"]


@admin.register(AssetAttribute)
class AssetAttributeAdmin(admin.ModelAdmin):
    list_display = ["asset", "code", "value_type", "storage_datapoint", "history_enabled"]


@admin.register(AssetRelationship)
class AssetRelationshipAdmin(admin.ModelAdmin):
    list_display = ["source", "target", "relation_type"]
