from django.contrib import admin
from . import models


class StudentAdmin(admin.ModelAdmin):
    list_display  = [field.name for field in models.Student._meta.fields]
class TransactionAdmin(admin.ModelAdmin):
    list_display  = [field.name for field in models.Transaction._meta.fields]
class FeesAdmin(admin.ModelAdmin):
    list_display  = [field.name for field in models.Fees._meta.fields]

admin.site.register(models.Student,StudentAdmin)
admin.site.register(models.Fees,FeesAdmin)
admin.site.register(models.Transaction,TransactionAdmin)
# admin.site.register(models.Transaction)