from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(News)
admin.site.register(AgriculturalTechnique)
admin.site.register(SchemeAdd)
admin.site.register(Crop)
admin.site.register(Solution)
admin.site.register(Feedback)
admin.site.register(FarmerProduct)
# admin.site.register(CartItem)
admin.site.register(FarmCart)
admin.site.register(FarmOrder)
