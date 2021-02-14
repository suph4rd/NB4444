from django.contrib import admin
from django.utils.safestring import mark_safe
from B4 import models


class NljAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_nlg', 'text_nlg', 'image_nlg_def')
    list_display_links = ('id', 'date_nlg')
    search_fields = ('date_nlg', 'text_nlg')

    def image_nlg_def(self, obj):
        if obj.image_nlg:
            return mark_safe(f'<img src="{obj.image_nlg.url}" width="100" >')
        else:
            return 'Фото отсутствует'


class MinfinAdmin(admin.ModelAdmin):
    list_display = ('id','get_type_table_display', 'date_create', 'balance', 'price', 'describe')
    list_display_links = ('id', 'get_type_table_display', 'date_create')
    search_fields = ('date_create', 'describe', 'get_type_table_display')


admin.site.register(models.StandartVichet)
admin.site.register(models.Nlg, NljAdmin)
admin.site.register(models.Minfin, MinfinAdmin)
