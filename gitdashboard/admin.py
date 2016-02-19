from django.contrib import admin
from .models import Repo, Branch 

admin.site.register(Repo)
admin.site.register(Branch)

# Register your models here.
