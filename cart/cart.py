
class Cart():

    def __init__(self,request):

        self.session = request.session


        ## RETURNING USER -- OBTAINING HIS EXISTING SESSION
        cart = self.session.get('session_key') 
     

        ##NEW USER - GENRATE A NEW SESION.
        if 'session_key' not in request.session:   

            cart = self.session['session_key'] = {}  

        self.cart = cart




    def add(self, product, product_qty): 

        product_id = str(product.id)  

        if product_id in self.cart:

            self.cart[product_id]['qty'] = product_qty

        else:

            self.cart[product_id] = {'price':str(product.price), 'qty':product_qty}

        self.session.modified = True





    def delete(self, product_identity):  ##product is actually product id

        product_id = str(product_identity)


        if product_id in self.cart:

            del self.cart[product_id]


        self.session.modified = True


    def update(self, product_identity, product_qty):

        prod_id = str(product_identity)
        prod_qty = product_qty

        if prod_id in self.cart:
            self.cart[prod_id]['qty'] = prod_qty
            

        self.session.modified = True

        



    def total_len(self):

        return sum(item['qty'] for item in self.cart.values())
    
    ## THE ABOVE USED INSTEAD OF BELOW
    # def __len__(self):
    #     return sum(item['qty'] for item in self.cart.values())
    
    

# for obtaing the current cart cost
    def total_cost(self):

        cost = 0

        for details in self.cart.values():
            cost += details['qty'] * float(details['price'])
        return cost

   
    ## clears cart to empty, like when we checkout with cart items
    def clear(self):

        del self.session['cart']

        self.session.modified = True











