from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.Quantity = item.Quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.Quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)



def place_order(request, total=0, Quantity=0):
    current_user= request.user
    
    
    cart_items= CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return render('store')
    
    
    grand_total =0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price* cart_item.Quantity)
        Quantity+=cart_item.Quantity
    tax = (2*total)/100
    grand_total= total + tax
        
    
    
    if request.method == 'POST':        
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all info in table
            data = Order()
            data.user = current_user
            data.first_name= form.cleaned_data['first_name']
            data.last_name= form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email= form.cleaned_data['email']
            data.address_line_1= form.cleaned_data['address_line_1']
            data.address_line_2= form.cleaned_data['address_line_2']
            data.country= form.cleaned_data['country']
            data.state= form.cleaned_data['state']
            data.city= form.cleaned_data['city']
            data.order_note= form.cleaned_data['order_note']
            data.order_total = grand_total 
            data.tax = tax
            data.ip= request.META.get('REMOTE_ADDR')
            data.save()
#gen order no.
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user= current_user, is_ordered=False, order_number=order_number)
            context={
                'order': order,
                'cart_items':cart_items,
                'total': total,
                'grand_total': grand_total,
                'tax' : tax,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


            