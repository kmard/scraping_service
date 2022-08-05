from django import forms
from scrapping.models import City,language



class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=False,
                                  widget=forms.Select(attrs={'class':'form-control'})
                                  )
    language = forms.ModelChoiceField(queryset=language.objects.all(),
                                      to_field_name='slug',
                                      required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'})
                                      )

