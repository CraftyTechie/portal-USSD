from django.contrib import admin

from .models import SpecialExam, Student
from .models import Unit
from .models import Transcript
from .models import fee
from .models import SupplementaryExam, ClearanceRequest
from .models import Year, MpesaIDs

admin.site.index_title = ("MMUST PORTAL")
admin.site.site_header = ("MMUST PORTAL ADMINISTRATION")
admin.site.site_title = "ADMIN"


admin.site.register(Student)
admin.site.register(Unit)
admin.site.register(Transcript)
admin.site.register(SupplementaryExam)
admin.site.register(SpecialExam)
admin.site.register(fee)
admin.site.register(Year)
admin.site.register(ClearanceRequest)
