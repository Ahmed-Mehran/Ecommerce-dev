from django.shortcuts import render

from .models import Category, Product

from django.shortcuts import get_object_or_404  ## so we first import this funtionality to get our object from database adn if that object
                                                ## doesnt exist, we are going to return 404 not found



# Create your views here.

## THIS LISST ALL THE PRODUCT OBJECTS IN OUR DB 
def store(request):

    all_products = Product.objects.all()

    context = {'my_products' : all_products}

    return render(request, 'store/store.html', context)


## THIS LIST ALL THE CATEGORY PRODUCTS AS DROP DOWN MENU
def categories(request):  

    all_categories = Category.objects.all()   

    context = {'all_categories': all_categories}

    return context


## THIS VIEW FUNCTION GIVES DETAILED DETAIL OF SINGULAR PRODUCT
def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug) 

    context = {'product': product}

    return render(request, 'store/product-info.html', context)

    

## This view function lists the categeories
def list_category(request, category_slug):  

    category_type = get_object_or_404(Category, slug=category_slug)   

    category_products = category_type.product.all()  

    context = {'category_products': category_products, 'category_name': category_type}

    return render(request, 'store/category-products.html', context)



   

