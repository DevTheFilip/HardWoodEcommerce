from django.contrib import admin

# Register your models here.


from .models import Category,Product


from django.contrib import admin

admin.site.site_header = "HARDWOOD PALLETS ADMIN PANNEL"
admin.site.site_title = "by Filip"
admin.site.index_title = "Welcome to the Filip's Advanced Store Admin Portal"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}