from django.contrib import admin
from product.models import Category, Product, Images
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent','status']
    list_filter = ['status']

class ProductImagesInline(admin.TabularInline):
    model = Images
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ['image_tag']
    inlines = [ProductImagesInline]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)