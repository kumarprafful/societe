from django.contrib import admin

from record.models import MonthlyRecord, Society, Member, SocietySetting
# Register your models here.

admin.site.register(Society,prepopulated_fields = {"slug": ("society_name",),})
admin.site.register(Member)
admin.site.register(MonthlyRecord, list_display=['member', 'month'])
admin.site.register(SocietySetting)
