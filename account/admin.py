from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from account.models import Relation, Profile

class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    extra = 1

class ExtendedUserAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(Relation)
admin.site.register(User,ExtendedUserAdmin)