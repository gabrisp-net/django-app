from django.contrib import admin

from members.models import ProductMembership, ItemMembership, VideoMembership, Membership


@admin.register(Membership)
class Admin_Membership(admin.ModelAdmin):
   pass
# Register your models here.
@admin.register(VideoMembership)
class Admin_VideoMembership(admin.ModelAdmin):
   pass

@admin.register(ItemMembership)
class Admin_ItemMembership(admin.ModelAdmin):
    pass


@admin.register(ProductMembership)
class Admin_ProductMembership(admin.ModelAdmin):
    pass