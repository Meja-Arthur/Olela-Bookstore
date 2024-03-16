
from django.http import HttpResponse
from django.template import loader
from .models import Book, BooksCategory, Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.http import HttpResponseServerError


from django.views import View
from .forms import CustomerRegistrationForm, CustomerprofileForm
from django.contrib import messages
# Create your views here.


def Homepage(request):
    books = Book.objects.order_by('-created_at')[:8]
    return render(request, 'index.html', {'books': books})

@login_required
def product_detail(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)

        host = request.get_host()

        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': book.price,
            'item_name': book.title,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}/payment-success/{book.id}/",
            'cancel_url': f"http://{host}/payment-failed/{book.id}/",

        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context = {
            'book': book,
            'paypal': paypal_payment
        }

        return render(request, 'product-single.html', context)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in product_detail view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")


def PaymentSuccessful(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'payment-success.html', {'book': book})

def paymentFailed(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'payment-failed.html', {'book': book})



@login_required
def download_book(request, book_id):
    try:
        book = get_object_or_404(Book, pk=book_id)
        file_path = book.file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + book.file.name.split('/')[-1]
            return response

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in product_detail view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")


def Shop(request):
    books = Book.objects.all()
    categories = BooksCategory.objects.all()

    #Filter books based on price range if the form is submitted

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        books = Book.filter_by_price_range(min_price, max_price)

    return render(request, 'shop.html',
                  {
                      'books': books,
                      'categories': categories
                   }
                  )


def Category_book(request, category_id):
    category = get_object_or_404(BooksCategory, pk=category_id)
    books = Book.objects.filter(category=category)
    return render(request, 'shop.html', {'category': category, 'books': books})




class CustomRegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = CustomerRegistrationForm()
        return render(request, 'register.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation! User Registration was  successfully.")

        else:
            messages.error(request, "Invalid cridentials please try again")
        return render(request, 'register.html', locals())


class ProfileView(View):

    def get(self,request):
        form = CustomerprofileForm()
        return render(request, 'profile.html', locals())
    def post(self,request):
        form = CustomerprofileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']


            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation! profile was  successfully saved.")
        else:
            messages.error(request, "Invalid cridentials please try again")

        return render(request, 'profile.html', locals())


@login_required
def Address(request):
    try:
        add = Customer.objects.filter(user=request.user)
        return render(request, 'address.html', locals())

    except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error in product_detail view: {e}")
            # Return a server error response
            return HttpResponseServerError("Sorry, something went wrong. Please try again later.")



def logout_view(request):
    logout(request)
    return redirect('/')












def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def blog(request):
    template = loader.get_template('blog.html')
    return HttpResponse(template.render())

def blogSingle(request):
    template = loader.get_template('blog-single.html')
    return HttpResponse(template.render())

def Cart(request):
    template = loader.get_template('cart.html')
    return HttpResponse(template.render())

def Checkout(request):
    template = loader.get_template('checkout.html')
    return HttpResponse(template.render())


# def ProductSingle(request):
#     template = loader.get_template('product-single.html')
#     return HttpResponse(template.render())