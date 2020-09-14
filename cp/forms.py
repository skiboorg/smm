from django.forms import ModelForm
from .models import *

class SocialNetworkAddForm(ModelForm):
    class Meta:
        model = SocialNetwork
        fields = ('name',
                  'icon',
                  )
        exclude = ()




class TarifAddForm(ModelForm):
    class Meta:
        model = Tarif
        fields = ('name',
                  'price',
                  'input_name',
                  'is_textarea',
                  'min',
                  'max',
                  'description',
                  )
        exclude = ()

