from django.contrib.auth.models import User
from django.db import models

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


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



class Customer(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     name = models.CharField(max_length=255)
     locality = models.CharField(max_length=200)
     city = models.CharField(max_length=200)
     mobile = models.IntegerField(default=0, blank=True)
     zipcode = models.IntegerField(default=0, blank=True)
     state = models.CharField(choices=STATE_CHOICES, max_length=100)

     def __str__(self):
         return self.name



class john(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
