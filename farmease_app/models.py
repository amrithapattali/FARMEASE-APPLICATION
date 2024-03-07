from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
import re
from django.contrib.auth.hashers import make_password

# Create your models here.
def contact_validate(value):
    rule = r"^[9876][0-9]{9}$"
    match = re.fullmatch(rule, value)
    if not match:
        raise ValidationError("Please enter a valid contact number")
    

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Farmer', 'Farmer'),
        ('User', 'User'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, blank=True, null=True,validators=[contact_validate])
    address = models.TextField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class SchemeAdd(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    scheme_name = models.CharField(max_length=100, null=True, blank=True)
    start_age = models.IntegerField(null=True)
    end_age = models.IntegerField(null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    # def contains_age(self, age_to_check):
    #     return self.start_age <= age_to_check <= self.end_age
    
    def __str__(self):
     if self.scheme_name:
        return self.scheme_name
     else:
        return "SchemeAdd Object ({})".format(self.pk)

    
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class AgricultureOffice(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.name
    
class AgriculturalTechnique(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='technique_images/', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class Crop(models.Model):
    techniques = models.ManyToManyField(AgriculturalTechnique, default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()
    climate = models.CharField(max_length=100)
    growth_period = models.CharField(max_length=100)
    harvesting_time = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Solution(models.Model):
    symptoms = models.CharField(max_length=255)
    solution = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.symptoms
    
class Feedback(models.Model):
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
class FarmerProduct(models.Model):
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    CROP_CHOICES = [
        ("Vegetables", "Vegetables"),
        ("Fruits", "Fruits"),
        ("Grains", "Grains"),
    ]
    crop_type = models.CharField(max_length=200, choices=CROP_CHOICES, default="Vegetables")
    crop_name = models.CharField(max_length=500,blank=True, null=True)
    image = models.ImageField(upload_to='product_images/',blank=True, null=True)  # Assuming you want to store product images
    price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)  # Assuming quantity is in grams
    description = models.TextField(null=True, blank=True)
    is_out_of_stock = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.is_out_of_stock = True
        elif self.quantity > 0:
            self.is_out_of_stock = False

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.crop_name
    
class FarmCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    posted_by = models.CharField(max_length=150, null=True, blank=True)
    crop_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='equipment/', null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.crop_name
    
    def update_quantity(self, quantity=None):
        old_quantity = self.quantity
        if quantity is not None:
            self.quantity = quantity
        else:
            self.quantity += 1
        self.price = self.price * (self.quantity / old_quantity)  # Adjust the price based on the new quantity
        self.save()


class FarmOrder(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    
    # Fields to store details of ordered items
    crop_names = models.TextField(null=True, blank=True)
    quantities = models.TextField(null=True, blank=True)
    prices = models.TextField(null=True, blank=True)

    total = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    estimated_date = models.DateField(blank=True, null=True)
    
    
    status_options = (
        ("order-placed", "order-placed"),
        ("cancelled", "cancelled"),
    )
    status = models.CharField(max_length=200, choices=status_options, default="order-placed")


    
# class Cart(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     items = models.ManyToManyField('FarmerProduct', through='CartItem')
#     total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

#     def __str__(self):
#         return f"Cart for {self.user.username}"

#     def update_total_price(self):
#         total_price = sum(item.total_price for item in self.cartitem_set.all())
#         self.total_price = total_price
#         self.save()

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey('FarmerProduct', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)
#     total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name} in cart for {self.cart.user.username}"

#     def save(self, *args, **kwargs):
#         self.total_price = self.product.price * self.quantity
#         super(CartItem, self).save(*args, **kwargs)
#         self.cart.update_total_price()
        
        
# class FarmOrder(models.Model):
#     username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     address = models.CharField(max_length=1000)
    
#     # Fields to store details of ordered items
#     crop_names = models.TextField(null=True, blank=True)
#     quantities = models.TextField(null=True, blank=True)
#     prices = models.TextField(null=True, blank=True)

#     total = models.DecimalField(decimal_places=2, max_digits=10, default=0)
#     order_date = models.DateTimeField(auto_now_add=True)
#     estimated_date = models.DateField(blank=True, null=True)
    
    
#     status_options = (
#         ("order-placed", "order-placed"),
#         ("cancelled", "cancelled"),
#     )
#     status = models.CharField(max_length=200, choices=status_options, default="order-placed")
        


class PlantImage(models.Model):
    image = models.ImageField(upload_to='plant_images/')


class PlantHealthResult(models.Model):
    is_healthy = models.BooleanField()
    name = models.CharField(max_length=255)
    probability = models.FloatField()
    description = models.TextField()
    treatment = models.TextField()

class healthFeedback(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    result = models.ForeignKey(PlantHealthResult, on_delete=models.CASCADE, related_name='feedback')
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    