from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES=(
    ('VT','Vitamini'),
    ('GG','Gigiena'),
    ('AB','Antibiotiki'),
    ('OB','Obezbalivaushie'),
    ('PT','Prostuda'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    image = models.ImageField(upload_to="product")
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    phone=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    def __str__(self):
        return self.name
   
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity *  self.product.price
    
class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.FloatField()
    order_id=models.CharField(max_length=100,blank=True,null=True)
    payment_status=models.CharField(max_length=100,blank=True,null=True)
    payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.PositiveBigIntegerField(default=1)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity* self.product.price
    
