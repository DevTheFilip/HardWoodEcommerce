from urllib import request

from django.shortcuts import render

from .forms import CreateUserForm, LoginForm, UpdateUserForm

from django.contrib.admin.views.decorators import staff_member_required
from payment.forms import ShippingForm
from payment.models import ShippingAddress

from payment.models import Order, OrderItem

from django.contrib.auth.models import User

from django.shortcuts import redirect

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages


from django.http import HttpResponse

# Create your views here.

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            #Email verification setup
            current_site = get_current_site(request)
            subject = "HardWoodPellets - Email Verification"
            message = render_to_string('account/registration/email-verification.html',{

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),


            })
            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')


    context = {'form': form}





    return render(request, 'account/registration/register.html',context = context)






def email_verification(request,uidb64,token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    #Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    else:
        #Failed
        return redirect('email-verification-failed')







def email_verification_sent(request):
    # Render the email verification sent page
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    # Render the email verification success page
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    # Render the email verification failed page
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
                return redirect('dashboard')

    context = {'form': form}
    return render(request,'account/my-login.html',context)


@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

#Logout

def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass

    messages.success(request, 'You have been logged out.')

    #auth.logout(request)
    return redirect('store')




# Profile management and delete account views
@login_required(login_url='my-login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)
    #updateing our user username and email
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profil actualizat cu succes.')
            return redirect('dashboard')

    context = {'user_form': user_form}


    return render(request, 'account/profile-management.html', context=context)



@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        messages.error(request, 'Account deleted successfully.')
        return redirect('store')


    return render(request, 'account/delete-account.html')


#shipping view
@login_required(login_url='my-login')
def manage_shipping(request):
    try:
        #Check if user has shipping address
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:
        #Account does not have shipping address
        shipping = None

    form = ShippingForm(instance=shipping)

    if(request.method == 'POST'):
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            #assing kf to obj
            shipping_user = form.save(commit=False)

            #adding the fk
            shipping_user.user = request.user
            shipping_user.save()

            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'account/manage-shipping.html', context=context)


@login_required(login_url='my-login')
def track_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set')
    context = {'orders': orders}
    return render(request, 'account/track-orders.html', context=context)



@staff_member_required(login_url='my-login')
def manage_orders(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("order_status")
        try:
            order = Order.objects.get(id=order_id)
            order.order_status = new_status
            order.save()
            messages.success(request, f"Statusul comenzii #{order.id} a fost actualizat la '{new_status}'.")
        except Order.DoesNotExist:
            messages.error(request, "Comanda nu a fost găsită.")

    orders = Order.objects.all().order_by('-date_odered')
    status_choices = ["Pending", "Processing", "Sent", "Delivered"]

    return render(request, "admin/manage-orders.html", {
        "orders": orders,
        "status_choices": status_choices
    })


from django.shortcuts import get_object_or_404, redirect

@staff_member_required(login_url='my-login')
def delete_order(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, f"Comanda #{order_id} a fost ștearsă cu succes.")
    else:
        messages.error(request, "Nu ai permisiunea să ștergi comenzi.")
    return redirect('manage-orders')

