from django.urls import path

from . import views


urlpatterns = [
    
    ## STORE MAIN PAGE URL PATH
    path('', views.store, name='store'),
    

    ## INDIVIDUAL PRODUCT URL PATH
    path('product/<slug:product_slug>/', views.product_info, name='product-info' ),  


    ## INDIVIDUAL CATEGORY URL PATH
    path('list-category/<slug:category_slug>/', views.list_category, name='list-category' ),  



]