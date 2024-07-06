from django.shortcuts import render

from .cart import Cart

from store.models import Product  
from django.shortcuts import get_object_or_404


from django.http import JsonResponse




# view cart details
def cart_summary(request):

    cart_instance = Cart(request) 

    cart_products = cart_instance.cart

    products_with_details = []

    total_price = cart_instance.total_cost()


    for product_id, details in cart_products.items():

        product = get_object_or_404(Product, id=product_id)

        products_with_details.append({

            'product': product,
            'qty': details['qty'],
            'price': details['price'],
            'total_item_price': details['qty'] * float(details['price']),

        })



    context = {'cart_products': products_with_details, 'total_price':total_price}

    return render(request,'cart/cart-summary.html' , context)






def cart_add(request):

    cart = Cart(request)
    

    if request.POST.get('action') == 'post':  ## see we write like this and not if request.method =='POST', because the call is from AJAX and also
                                              ## post is to be written in small letters, as if you see in product-info.html, for AJAX request, we 
                                              ## have action = 'post' and not 'POST'

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity')) 

        product = get_object_or_404(Product, id=product_id) 

        cart.add(product=product, product_qty=product_quantity)  

        total_cart_quantity = cart.total_len()

        # response = {'qty': product_quantity}
        response = {'qty': total_cart_quantity}


        return JsonResponse(response)





## if we want to delete something in the cart
def cart_delete(request):

    cart = Cart(request)
    

    if request.POST.get('action') == 'post': 


        product_id = int(request.POST.get('product_id'))

        cart.delete(product_identity=product_id)  

        cart_total = cart.total_cost()  

        total_cart_quantity = cart.total_len()

         
        response = {'qty': total_cart_quantity, 'total':cart_total}


        return JsonResponse(response)





## if we want to update the cart e.g update the quantity of Product(like nike shoes)
def cart_update(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':  

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product_identity=product_id, product_qty=product_quantity)

        cart_total = cart.total_cost()  

        total_cart_quantity = cart.total_len()

        response = {'qty': total_cart_quantity, 'total':cart_total}


        return JsonResponse(response)





