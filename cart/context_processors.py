
from .cart import Cart



def cart(request):

    return {'cart': Cart(request)}   

## THE ABOVE CAN BE WRITTEN AS 
# def cart(request):

#     cart = Cart(request)
#     return {'cart': cart}