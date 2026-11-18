from django.contrib import admin

from dashboards.models import Dashboard, Widget


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ["name", "tenant", "project"]


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ["dashboard", "title", "widget_type", "x", "y"]
