from django.contrib import admin

from record.models import MonthlyRecord, Society, Member
# Register your models here.

admin.site.register(Society)
admin.site.register(Member)
admin.site.register(MonthlyRecord)
