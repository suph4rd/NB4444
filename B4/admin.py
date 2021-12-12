from django.contrib import admin
from django.utils.safestring import mark_safe

from B4 import models


@admin.register(models.Note)
class NljAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'text', 'get_image')
    list_display_links = ('id', 'created_at')
    search_fields = ('created_at', 'text')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" >')
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


admin.site.register(models.DefaultDeductions)
