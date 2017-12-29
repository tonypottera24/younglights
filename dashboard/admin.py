from django.contrib import admin

from .models import UserProfile
from .models import MentoringRelationship, MentoringRecord, Mission
from .models import ApplyCountry, ApplySchool, ApplyCollege, ApplyMajor, ApplyDegree, ApplyDegreeType, ApplySemester, ApplyGRESubject

# Register your models here.
admin.site.register(UserProfile)

admin.site.register(MentoringRelationship)
admin.site.register(MentoringRecord)
admin.site.register(Mission)

admin.site.register(ApplyCountry)
admin.site.register(ApplySchool)
admin.site.register(ApplyCollege)
admin.site.register(ApplyMajor)
admin.site.register(ApplyDegree)
admin.site.register(ApplyDegreeType)
admin.site.register(ApplySemester)
admin.site.register(ApplyGRESubject)

from django.contrib.auth.models import Permission
admin.site.register(Permission)
