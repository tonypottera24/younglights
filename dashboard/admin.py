from django.contrib import admin

from .models import UserProfile
from .models import MentoringRelationship, MentoringRecord, Mission

# Register your models here.
admin.site.register(UserProfile)

admin.site.register(MentoringRelationship)
admin.site.register(MentoringRecord)
admin.site.register(Mission)

from django.contrib.auth.models import Permission
admin.site.register(Permission)
