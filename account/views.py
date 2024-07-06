from django.shortcuts import render,  redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UpdateUserForm

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site  

from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate


from django.contrib.auth.decorators import login_required


## IMPORTED FROM PAYMENT APP
from payment.forms import ShippingForm
from payment.models import ShppingAddress



def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)  ## retrieve the data entered in form and store in form variable

        if form .is_valid():

            user = form.save()

            user.is_active = False

            user.save()

            ## email verification setup 

            current_site = get_current_site(request)
 
            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html', {

                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')


        
    context = {'RegistrationForm':form}

    return render(request, 'account/registration/register.html', context)



def verification_of_email(request, uidb64, token_value):

    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # VERIFIED SUCCESSFULLY

    if user and user_tokenizer_generate.check_token(user, token_value):

        user.is_active = True

        user.save()

        return redirect('email-verification-success') 
    
    ## NOT VERIFIED
    
    else:

        return redirect('email-verification-failed')




def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')



def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')



def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')




def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)
        if form.is_valid():

            username = request.POST.get('username') 
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)  

            if user is not None: 

                auth.login(request, user) 

                return redirect("dashboard")
            
    context = {'LoginForm':form}

    return render(request, 'account/my-login.html', context)



def user_logout(request):

    auth.logout(request)

    return redirect("store")



    

@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'account/dashboard.html')






@login_required(login_url='my-login')
def profile_management(request):

    current_user = request.user

    form  = UpdateUserForm(instance=current_user)

    if request.method == 'POST':

        form = UpdateUserForm(request.POST, instance=current_user)


        if form.is_valid():

            form.save()

            return redirect('dashboard')
        
    context = {'ProfileForm':form}

    return render(request, 'account/profile-management.html', context)



@login_required(login_url='my-login')
def delete_account(request):

    current_user = request.user.id

    user = User.objects.get(id=current_user)

    if request.method == 'POST':

        user.delete()
        
        return redirect('store')
    
    return render(request, 'account/delete-account.html')



## shipping address view
@login_required(login_url='my-login')
def manage_shipping(request):

    current_user = request.user.id

    try:
        shipping = ShppingAddress.objects.get(user=current_user)

    except ShppingAddress.DoesNotExist:

        shipping = None
    
  #  shipping = ShppingAddress.objects.get(user=current_user) 

    if shipping is None:  ## If no shipping address exists, handle form creation, means the user has never created or filled any user form and is doing for the first time

        form = ShippingForm()

        if request.method == 'POST':

            form = ShippingForm(request.POST)

            if form.is_valid(): 

                shipping_user = form.save(commit=False)

                shipping_user.user = request.user  ##  adding foreign key instance of user manually
                shipping_user.save()

                return redirect('dashboard')


    else:  ## If a shipping address exists, handle form update means if the shipping form is to be updated 

        form = ShippingForm(instance=shipping)

        if request.method == 'POST':

            form = ShippingForm(request.POST, instance=shipping)

            if form.is_valid(): 

                form.save()

                return redirect('dashboard')
            
    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context)



