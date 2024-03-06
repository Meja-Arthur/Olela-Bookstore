from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.Homepage, name='index'),
    path('product/<int:book_id>/', views.product_detail, name='product_detail'),
    path('download_book/<int:book_id>/', views.download_book, name='download_book'),


    path('payment-success/<int:book_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:pbook_id>/', views.paymentFailed, name='payment-failed'),

    path('shop/', views.Shop, name='shop'),
    path('category/<int:category_id>/', views.Category_book, name='category_books'),









    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog-single/', views.blogSingle, name='blog-single'),
    path('cart/', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),

    # path('product-single/', views.ProductSingle, name='product-single')

]