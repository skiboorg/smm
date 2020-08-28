from django.db import models
import uuid



class SocialNetwork(models.Model):
    discount = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=False, null=True)
    icon = models.ImageField(upload_to='services/', blank=False, null=True)
    slogan = models.CharField(max_length=255, blank=False, null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    pass

class Service(models.Model):
    social_network = models.ForeignKey(SocialNetwork,on_delete=models.CASCADE,blank=False,null=True,related_name='services')
    name = models.CharField(max_length=255, blank=False, null=True)

class Tarif(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE,blank=False,null=True,related_name='tarifs')
    name = models.CharField(max_length=255, blank=False, null=True)
    price = models.DecimalField(decimal_places=2,max_digits=5,default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    description = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ['price']

class Status(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    css_class = models.CharField(max_length=255, blank=False, null=True)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    social_network = models.ForeignKey(SocialNetwork,on_delete=models.CASCADE,blank=False,null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=False, null=True)
    tarif = models.ForeignKey(Tarif, on_delete=models.CASCADE, blank=False, null=True)
    total_number = models.IntegerField(default=0)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=False,null=True)
    url = models.CharField(max_length=255,blank=False,null=True)
    email = models.CharField(max_length=255,blank=False,null=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    is_new = models.BooleanField(default=True)


