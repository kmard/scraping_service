
# https://docs.djangoproject.com/en/3.0/topics/auth/default/
from django import forms
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.hashers import check_password
from scrapping.models import language,City


User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-comtrol'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-comtrol'}))

    def clean(self, *args,**kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User is not defined !')

            if not check_password(password,qs[0].password):
                raise forms.ValidationError('Wrong password !')

            user = authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError('Account is disabled !')

            return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='enter email',
        widget=forms.EmailInput(attrs={'class':'form-comtrol'}))
    password = forms.CharField(label='enter password',
        widget=forms.PasswordInput(attrs={'class':'form-comtrol'}))
    password2 = forms.CharField(label='repeat password',
        widget=forms.PasswordInput(attrs={'class': 'form-comtrol'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords are different!')
        else:
            return data['password2']

class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=True,
                                  widget=forms.Select(attrs={'class':'form-control'}),
                                  label='City'
                                  )
    language = forms.ModelChoiceField(queryset=language.objects.all(),
                                      to_field_name='slug',
                                      required=True,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Program language'
                                      )

    send_email = forms.BooleanField(required=False,
                                    widget=forms.CheckboxInput,
                                    label='Send email')


    class Meta:
        model = User
        fields = ('city','language','send_email')

    class ContactForm(forms.Form):
        pass

class ContactForm(forms.Form):
    city = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Language'
    )
    email = forms.EmailField(
        label='Введите имэйл', required=True, widget=forms.EmailInput(
            attrs={'class': 'form-control'})
    )