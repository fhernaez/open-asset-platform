from django.apps import AppConfig


class AssetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "assets"
    label = "assets"

    def ready(self) -> None:
        from django.db.models.signals import post_save

        from assets.signals import seed_catalog_on_tenant_create

        post_save.connect(
            seed_catalog_on_tenant_create,
            sender="platforms.Tenant",
            dispatch_uid="assets_seed_catalog_on_tenant_create",
        )
