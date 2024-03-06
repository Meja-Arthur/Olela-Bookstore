from django.db import models



# Create your models here.
class BooksCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):

     title = models.CharField(max_length=255)
     category = models.ForeignKey(BooksCategory, on_delete=models.CASCADE, related_name='products')
     pages = models.IntegerField()
     author = models.CharField(max_length=100)

     description = models.TextField(blank=True)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     image = models.ImageField(upload_to='book_images/', blank=True, null=True)
     file = models.FileField(upload_to='books/')
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.title

     @classmethod
     def filter_by_price_range(cls, min_price, max_price):
         """
         Custom method to filter books by price range.
         """
         return cls.objects.filter(price__gte=min_price, price__lte=max_price)