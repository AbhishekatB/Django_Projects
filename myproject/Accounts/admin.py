from django.contrib import admin
from .models import User,Customer,Nursery_Manager,Plants,Images

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Nursery_Manager)
admin.site.register(Plants)
admin.site.register(Images)