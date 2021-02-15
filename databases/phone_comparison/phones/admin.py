from django.contrib import admin
from .models import PhoneGeneric, PhoneApple, PhoneSamsung, PhoneXiaomi


# Register your models here.
@admin.register(PhoneGeneric)
class PhoneGenericAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneApple)
class PhoneGenericAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneSamsung)
class PhoneGenericAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneXiaomi)
class PhoneGenericAdmin(admin.ModelAdmin):
    pass
