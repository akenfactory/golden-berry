from django.contrib import admin
from commons.models import History, PlanXService, TmpHistory


# Register your models here.
admin.site.register(PlanXService)
admin.site.register(History)
admin.site.register(TmpHistory)