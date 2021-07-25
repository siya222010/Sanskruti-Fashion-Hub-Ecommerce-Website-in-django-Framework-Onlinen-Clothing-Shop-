from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=250)
    useremail = models.EmailField(max_length=100)
    userpassword= models.CharField(max_length=25)
    usermobileno = models.BigIntegerField()

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
   

class Subcategory(models.Model):
    cat = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Subcategory_two(models.Model):
    cat_sub = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    cat_sub_two = models.ForeignKey(Subcategory_two,on_delete=models.CASCADE)
    p_name = models.CharField(max_length=250)
    p_price = models.FloatField()
    p_size = models.CharField(max_length=20)
    img = models.ImageField(upload_to="product_image")
    desc = models.TextField()

    def __str__(self):
        return self.p_name

class Cart(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    total = models.IntegerField()
    qauntity = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.p_name


class Order(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    fullname = models.CharField(max_length=250)
    mobileno = models.BigIntegerField()
    landmark = models.TextField(max_length=450) 
    town = models.TextField(max_length=50)
    state = models.TextField(max_length=50)
    addresstype = models.TextField(max_length=50)

    def __str__(self):
        return self.fullname


class Subscribe(models.Model):
    email =  models.EmailField(max_length=100)
    def __str__(self):
        return self.email






















