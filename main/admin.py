from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CS_User)

admin.site.register(Service)
admin.site.register(Service_category)
admin.site.register(Partners)
admin.site.register(Order)