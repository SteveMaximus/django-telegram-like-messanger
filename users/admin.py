from django.contrib import admin
from .models import Messages
from .models import Rubric
from .models import Profile
# Register your models here.

admin.site.register(Rubric)
admin.site.register(Messages)
admin.site.register(Profile)