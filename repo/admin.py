from repo.models import Repo
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.unregister(Site)
admin.site.unregister(Group)

class RepoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'email', 'repo', 'location', 'longitude', 'latitude', 'enabled')

admin.site.register(Repo, RepoAdmin)
