from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Laden, Einkauf


@admin.register(Laden)
class LadenAdmin(admin.ModelAdmin):
    list_display = ['name', 'reihenfolge']
    ordering = ['reihenfolge', 'name']


@admin.register(Einkauf)
class EinkaufAdmin(admin.ModelAdmin):
    list_display = ['artikel', 'laden', 'gekauft', 'geaendert', 'erstellt_von']
    list_filter = ['gekauft', 'laden']
    search_fields = ['artikel']
    readonly_fields = ['geaendert', 'erstellt', 'erstellt_von']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.erstellt_von = request.user
        super().save_model(request, obj, form, change)


# Customize admin site
admin.site.site_header = 'Einkaufsliste Administration'
admin.site.site_title = 'Einkaufsliste'
admin.site.index_title = 'Verwaltung'
