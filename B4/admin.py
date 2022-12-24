from django.contrib import admin
from django.utils.safestring import mark_safe

from B4 import models, mixins, admin_filters


@admin.register(models.Note)
class NoteAdmin(mixins.AdminQsManagerMixin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'text', 'get_image')
    list_display_links = ('id', 'created_at')
    search_fields = ('created_at', 'text')
    list_filter = ('is_delete', admin_filters.NoteImageExistFilter, admin_filters.NoteTextExistFilter)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" >') if obj.image else 'Фото отсутствует'
    get_image.short_description = "Фото"


@admin.register(models.Plan)
class PlanAdmin(mixins.AdminQsManagerMixin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'name', 'user')
    list_display_links = ('id', 'created_at')
    list_filter = ('is_delete', )


@admin.register(models.Task)
class TaskAdmin(mixins.AdminQsManagerMixin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'plan', 'section', 'description', 'is_ready', 'priority')
    list_display_links = ('id', 'created_at')
    list_filter = ('is_delete',)


@admin.register(models.DefaultDeductions)
class DefaultDeductionsAdmin(mixins.AdminQsManagerMixin, admin.ModelAdmin):
    list_filter = ('is_delete', )


admin.site.register(models.Section)
