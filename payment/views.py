from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


## IMPORTED FROM PAYMENT APP
from payment.forms import ShippingForm
from payment.models import ShppingAddress

from .models import Order, OrderItem

from store.models import Product

## IMPORT CART.PY
from cart.cart import Cart


@login_required(login_url='my-login')
def checkout(request):

   
    current_user = request.user.id

    try:
        shipping = ShppingAddress.objects.get(user=current_user)

    except ShppingAddress.DoesNotExist:
        shipping = None



    if shipping is None:  

        form = ShippingForm()

        if request.method == 'POST':

            form = ShippingForm(request.POST)

            if form.is_valid():

                shipping_user = form.save(commit=False)
                shipping_user.user = request.user ##  adding foreign key instance of user manually
                shipping_user.save()

                return redirect('order-confirmation')

    else: 

        form = ShippingForm(instance=shipping)

        if request.method == 'POST':
            form = ShippingForm(request.POST, instance=shipping)

            if form.is_valid():

                form.save()
                return redirect('order-confirmation')
            
            
    context = {'CheckoutForm': form}

    return render(request, 'payment/checkout.html', context)



    

def order_confirmation(request):

    ## Grabbing CART DETAILS of user

    cart_instance = Cart(request) 

    cart_products = cart_instance.cart

    products_details = []

    total_cart_price = cart_instance.total_cost()

    for product_id, details in cart_products.items():

        product = get_object_or_404(Product, id=product_id)

        products_details.append({

            'product': product,
            'quantity': details['qty'],
            'price': details['price'],
            'total_item_price': details['qty'] * float(details['price']),
            
        })


    ## Grabbing shipping details of user

    current_user = request.user

    shipping = get_object_or_404(ShppingAddress, user=current_user)
    

    order = {

        'full_name' : shipping.full_name,

        'email' : shipping.email,

        'shipping_address': (shipping.address1  + "\n" + shipping.address2  + "\n" + shipping.city ),

        'amount_paid' : total_cart_price,

    }



    context = {'Main_Order' : order, 'Order_Item':products_details}  


    return render(request, 'payment/order-confirmation.html', context)




########  CONFIRM PAYMENT AND SAVING TO DATABASE ON CONFIRMING VIEW FUNCTION -- EXPLANATION THIS IS PENDING




def save_order(request):

    current_user = request.user

    shipping = get_object_or_404(ShppingAddress, user=current_user)
    

    if request.POST.get('action') == 'post':
        

        name_full = request.POST.get('full_name') # 'full_name' in request.post is we getting data from AJAX request and rest of below as well

        email_id = request.POST.get('email')

        total_amount = request.POST.get('amount_paid')

        shipping_address_full = (shipping.address1  + "\n" + shipping.address2  + "\n" + shipping.city ) ## I was not able to get the full shipping address by AJAX request as its too large for AJAX request to process
                                                                                                         # so for this I simply used the ShppingAddress model and got the address

        cart_instance = Cart(request)

       ## GRABBING THE DATA FROM ABOVE DATA GOT FROM AJAX AND STORING THE DATA IN ORDER MODEL

        order = Order.objects.create(full_name=name_full, email=email_id, shipping_address=shipping_address_full, amount_paid=total_amount, user=request.user)


        ## NOW WE WILL GRAB FROM CART.PY AND STORE THE DATA FOR ORDER ITEM MODEL

        cart_products = cart_instance.cart

        products_details = []


        for product_id, details in cart_products.items():

            product = get_object_or_404(Product, id=product_id)

            products_details.append({

                'product': product,
                'qty': details['qty'],
                'price': details['price'],
                'total_item_price': details['qty'] * float(details['price']),
                
            })

        ## Filling out the OrderItem model

        for item in products_details:

            OrderItem.objects.create(

                order=order,

                product=item['product'],

                quantity=item['qty'],

                price=item['total_item_price'],

                user=request.user
            )
        
    order_success = True

    response = JsonResponse({'success':order_success})

    return response    





            



def payment_success(request):

    ## once we are directed to this that is our order placement and paymnent was success full, and that makes sense, we would be only redirected here if it was a success
    ## so once on this we want to clear out the items in cart i.e we want to restore the cart to 0 as obviosuly items were bought

    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]

    return render(request, 'payment/payment-success.html')


def payment_failed(request):

    return render(request, 'payment/payment-failed.html')



def my_orders(request):


    
    order_items = OrderItem.objects.filter(order__user=request.user)

    context = {'order_items': order_items}

    return render(request, 'payment/my-orders.html', context)

































# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Configure PayPal SDK
# paypalrestsdk.configure({
#     "mode": "sandbox", # or "live" for production
#     "client_id": "Aboe3T79DjPei9iXRAyzbx3EQJevz7bGdM8YLFIrjANM3SL3973HzKEYnoIEiBmx-1LJrow_qu9M8KE8",
#     "client_secret": "EJSI1tuXov5WrPNcxAUlC2eYmzwC9EfDRB885bID_ycM-UH0jefbmyA6x7EIujwR2W-cBXbc6hnuWhR0"
# })




# @csrf_exempt
# def save_order(request):
#     if request.method == 'POST':

#         data = json.loads(request.body)

#         order_id = data['orderID']

#         payer_id = data['payerID']

#         order_details = data['orderDetails']

#         try:
#             payment = paypalrestsdk.Payment.find(order_id)

#             if payment and payment.payer.payer_info.payer_id == payer_id and payment.state == "approved":

#                 # Payment is valid
#                 order = Order.objects.create(

#                     full_name=order_details['fullName'],
#                     email=order_details['email'],
#                     shipping_address=order_details['shippingAddress'],
#                     amount_paid=order_details['amountPaid'],
#                     user=request.user

#                 )

#                 for item in order_details['products']:

#                     OrderItem.objects.create(
#                         order=order,
#                         product_id=item['product']['id'],
#                         quantity=item['quantity'],
#                         price=item['price'],
#                         user=request.user

#                     )

#                 return JsonResponse({'status': 'success'})
            
#             else:
#                 # Payment is not valid
#                 return JsonResponse({'status': 'failed'}, status=400)
            
#         except paypalrestsdk.ResourceNotFound as error:

#             logging.error(f"Payment not found: {error}")

#             return JsonResponse({'status': 'failed'}, status=400)