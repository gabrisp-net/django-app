from .models import Product, ProductImage, ProductTag, ProductSpecs, ProductVariation
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdminTag(admin.StackedInline):
    model = ProductTag


class ProductVariationAdmin(admin.StackedInline):
    model = ProductVariation
class ProductSpecsAdmin(admin.StackedInline):
    model = ProductSpecs

@admin.action(description="Publish")
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)

@admin.action(description="Unpublish")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, ProductSpecsAdmin, ProductVariationAdmin]
    list_display = ['title', 'price', 'preview']
    order_by = "latest_update"
    actions = [make_published, make_unpublished]
    class Meta:
        model = Product






