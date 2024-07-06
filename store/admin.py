from django.contrib import admin

# Register your models here.

from .models import Category, Product


## OLD WAY OF REGISTERING

# admin.site.register(Category)

# admin.site.register(Product)


## NEW WAY TO REGISTER WITH PRE POPULATED FIELDS


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):       
  
    prepopulated_fields = {'slug':('name',)}




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):       

    
    prepopulated_fields = {'slug':('title',)}


