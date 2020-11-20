from django.contrib import admin
from django.utils.safestring import mark_safe

from B4.models import standart_vichet, nlg, minfin, eda, transport, razvlechenia, amortizatia, prochee, nds

class NljAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_nlg', 'text_nlg', 'image_nlg_def')
    list_display_links = ('id', 'date_nlg')
    search_fields = ('date_nlg', 'text_nlg')

    def image_nlg_def(self, obj):
        if obj.image_nlg:
            return mark_safe(f'<img src="{obj.image_nlg.url}" width="100" >')
        else:
            return 'Фото отсутствует'

    image_nlg_def.short_description = 'Фотоотчёт'


admin.site.register(standart_vichet)
admin.site.register(nlg, NljAdmin)
admin.site.register(minfin)
admin.site.register(eda)
admin.site.register(transport)
admin.site.register(razvlechenia)
admin.site.register(amortizatia)
admin.site.register(prochee)
admin.site.register(nds)
