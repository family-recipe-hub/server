from django.contrib import admin
from .models import User, Profile, Language, ProfileLanguage


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Language)
admin.site.register(ProfileLanguage)
