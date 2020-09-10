from django.db import models
import uuid
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string

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

    def get_low_price(self):
        return self.tarifs.first().price
    def get_discount(self):
        return self.tarifs.first().price_w_discount
    def tarif_id(self):
        return self.tarifs.first().id

class Tarif(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE,blank=False,null=True,related_name='tarifs')
    name = models.CharField(max_length=255, blank=False, null=True)
    price = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    price_w_discount = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    description = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ['price']

class Status(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    css_class = models.CharField(max_length=255, blank=False, null=True)

class Order(models.Model):
    uu = models.CharField(max_length=255,default=uuid.uuid4)
    social_network = models.ForeignKey(SocialNetwork,on_delete=models.CASCADE,blank=False,null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=False, null=True)
    tarif = models.ForeignKey(Tarif, on_delete=models.CASCADE, blank=False, null=True)
    total_number = models.IntegerField(default=0)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True,null=True,default=1)
    url = models.CharField(max_length=255,blank=False,null=True)
    email = models.CharField(max_length=255,blank=False,null=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    is_new = models.BooleanField(default=True)
    is_payed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True)




def order_post_save(sender, instance, created, **kwargs):
    msg_html = render_to_string('email/admin.html', {'network': instance.social_network.name,
                                                     'service': instance.service.name,
                                                     'tarif': instance.tarif.name,
                                                     'number': instance.total_number,
                                                     'price': instance.total_cost,
                                                     })
    send_mail(f'Новый заказ ', None, 'support@ravesme.com',
              ['yusifowali@gmail.com'],
              fail_silently=False, html_message=msg_html)
    if instance.is_payed:
        msg_html = render_to_string('email/client.html',{'uuid':instance.uu})
        send_mail(f'Заказ успешно размещен', None, 'support@ravesme.com',
                  [instance.email],
                  fail_silently=False, html_message=msg_html)



post_save.connect(order_post_save, sender=Order)


class Payment(models.Model):
    payment_id=models.CharField(max_length=255,null=True,blank=True)
    payment_url=models.TextField(null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=False,null=True)
    amount = models.DecimalField('Сумма', decimal_places=2,max_digits=10,default=0)
    status = models.BooleanField('Статус платежа',default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True)

    class Meta:
        ordering = ('-id',)