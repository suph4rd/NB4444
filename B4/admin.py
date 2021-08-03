from django.contrib import admin
from django.utils.safestring import mark_safe
from B4 import models


@admin.register(models.Nlg)
class NljAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'text_nlg', 'image_nlg_def')
    list_display_links = ('id', 'created_at')
    search_fields = ('created_at', 'text_nlg')

    def image_nlg_def(self, obj):
        if obj.image_nlg:
            return mark_safe(f'<img src="{obj.image_nlg.url}" width="100" >')
        else:
            return 'Фото отсутствует'


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'name', 'user')
    list_display_links = ('id', 'created_at')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'plan', 'section', 'description', 'is_ready')
    list_display_links = ('id', 'created_at')


@admin.register(models.Section)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_active', 'name')
    list_display_links = ('id', 'created_at')


admin.site.register(models.StandartVichet)
