from django.contrib import admin
from .models import Product, Variation, ProductGallery

# import admin_thumbnails
# Register your models here.


# @admin_thumbnails.thumbnail('image')
# class ProductGalleryInline(admin.TabularInline):
#     model = ProductGallery
#     extra = 1



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','p_slug', 'product_description', 'price', 'stock', 'is_available', 'category' , 'created_date', 'modified_date','product_image')
    prepopulated_fields = { 'p_slug' : ('product_name', )}  

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'variation_category', 'variation_value', 'is_active' )
    list_editable = ('is_active',)
    list_filter   = ('product_name', 'variation_category', 'variation_value', 'is_active' )
    
admin.site.register(ProductGallery)
